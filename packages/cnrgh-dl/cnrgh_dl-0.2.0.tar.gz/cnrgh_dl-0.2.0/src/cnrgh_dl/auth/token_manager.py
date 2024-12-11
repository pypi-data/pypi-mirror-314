import math
import threading
from time import sleep
from typing import cast

import requests
from requests import Response
from typing_extensions import Self

from cnrgh_dl import config
from cnrgh_dl.auth.device_flow import DeviceFlow
from cnrgh_dl.config import REQUESTED_ACCESS_SCOPE
from cnrgh_dl.exceptions import MissingScopesError
from cnrgh_dl.logger import Logger
from cnrgh_dl.models import TokenErrorResponse, TokenResponse
from cnrgh_dl.utils import hash_access_token, safe_parse_obj_as, verify_scopes

logger = Logger.get_instance()
"""Module logger instance."""


class TokenManager:
    """Manages the lifecycle of an access token.
    When initialised, the class starts an OAuth 2.0 Device Authorization Grant process (Device Flow) to obtain one.
    Then, the access token can be refreshed using a daemon.
    If any error occurs while trying to refresh the access token, the daemon will stop.
    """

    has_refresh_daemon_stopped: bool
    """``True`` if the refresh token daemon has stopped, ``False`` otherwise."""
    _stop_refresh_daemon: bool
    """Set to ``True`` to stop the refresh token daemon, ``False`` by default."""
    _refresh_daemon_error: bool
    """``True`` if the refresh token daemon has encountered an error while running, ``False`` otherwise."""
    _token_response_lock: threading.Lock
    """Lock used to read and update the ``_token_response`` attribute."""
    _token_response: TokenResponse
    """Contains the access token and the refresh token returned by the Keycloak server."""
    _userinfo: dict[str, str]
    """User info dict returned by the Keycloak userinfo endpoint."""

    def __init__(self: Self) -> None:
        """Initialize the token manager by starting a device flow to obtain an access token and
        retrieve user info.
        """
        logger.debug("Initializing the token manager.")

        # Initialise refresh daemon related booleans.
        self.has_refresh_daemon_stopped = False
        self._stop_refresh_daemon = False
        self._refresh_daemon_error = False

        # Start the device flow to obtain an access and a refresh token.
        self._token_response_lock = threading.Lock()
        self._set_token_response(DeviceFlow.start())
        self._userinfo = self._get_userinfo()

        try:
            username = self._userinfo["name"]
        except KeyError:
            username = self._userinfo["preferred_username"]

        logger.info("Logged as: %s.", username)
        logger.debug(
            "Access token hash = %s.",
            hash_access_token(self.token_response.access_token),
        )

    @property
    def token_response(self: Self) -> TokenResponse:
        """Get the current valid access token.

        :return: A TokenResponse instance containing among other attributes an
            access and a refresh token.
        """
        with self._token_response_lock:
            return self._token_response

    def _set_token_response(self, token_response: TokenResponse) -> None:
        """Set the current valid access token."""
        with self._token_response_lock:
            self._token_response = token_response

    def _get_userinfo(self: Self) -> dict[str, str]:
        """Get user information by calling the Keycloak userinfo endpoint.

        :raises requests.exceptions.RequestException:
            An error occurred with the request.
        :return: A dict of string containing user information.
        """
        response: Response = requests.get(
            config.KEYCLOAK_USER_INFO_ENDPOINT,
            headers={
                "Authorization": f"Bearer {self.token_response.access_token}",
            },
            timeout=config.REQUESTS_TIMEOUT,
        )
        response.raise_for_status()
        return cast(dict[str, str], response.json())

    def _get_token_refresh_wait_time(self: Self) -> int:
        """Get the time (in seconds) to wait before trying to refresh the access token.
        The wait time is equal to 90% of the access token lifespan,
        leaving a 10% margin to refresh the access token before it expires.
        """
        expires_in = self.token_response.expires_in
        return expires_in - math.ceil(expires_in / 10)

    def _refresh_token(self: Self) -> None:
        """Refresh the current access token by calling the Keycloak token endpoint
        with its refresh token and save its new value.

        :raises requests.exceptions.RequestException:
            An error occurred with the request.
        """
        params: dict[str, str] = {
            "client_id": config.KEYCLOAK_CLIENT_ID,
            "scope": config.REQUESTED_ACCESS_SCOPE,
            "grant_type": "refresh_token",
            "refresh_token": self.token_response.refresh_token,
        }

        response = requests.post(
            config.KEYCLOAK_TOKEN_ENDPOINT,
            data=params,
            timeout=config.REQUESTS_TIMEOUT,
        )
        response.raise_for_status()

        self._set_token_response(
            safe_parse_obj_as(
                TokenResponse,
                response.json(),
            )
        )

    def _refresh_token_daemon(self: Self) -> None:
        """Wrapper around the _refresh_token() function for use within a daemon thread.
        If the function encounters any error, the function will exit, stopping the daemon thread.
        """
        # Obtain a refresh wait time based on the lifespan of the access token obtained during
        # the initialization of the TokenManager class.
        # As the loop waits first, this avoids directly refreshing the obtained token.
        wait_time = self._get_token_refresh_wait_time()
        previous_expires_in = -1
        logger.debug("[Refresh token] Starting background refresh...")

        while not (self._refresh_daemon_error or self._stop_refresh_daemon):
            logger.debug(
                "[Refresh token] Access token will expire in %s seconds, "
                "sleeping %s seconds before trying to refresh it.",
                self.token_response.expires_in,
                wait_time,
            )
            sleep(wait_time)

            logger.debug(
                "[Refresh token] Old access token hash = %s.",
                hash_access_token(self.token_response.access_token),
            )

            try:
                self._refresh_token()
                logger.debug(
                    "[Refresh token] New access token hash = %s.",
                    hash_access_token(self.token_response.access_token),
                )
                # Ensure that the server granted all the required scopes.
                verify_scopes(REQUESTED_ACCESS_SCOPE, self.token_response.scope)
                # Check that the expires_in property is not decreasing, indicating the end of the offline session.
                # In this case, stop the refresh token daemon.
                expires_in = self._token_response.expires_in
                if previous_expires_in > expires_in:
                    logger.warning(
                        "Offline session is about to end, "
                        "thus cnrgh-dl will stop refreshing the access token (still valid for %s seconds).",
                        expires_in,
                    )
                    self._stop_refresh_daemon = True
                else:
                    previous_expires_in = expires_in

            except requests.exceptions.RequestException as err:
                # Stop the refresh loop.
                self._refresh_daemon_error = True
                # If the token endpoint returns an HTTP error,
                # use the error response type and description when logging.
                if isinstance(err, requests.exceptions.HTTPError):
                    response_error: TokenErrorResponse = safe_parse_obj_as(
                        TokenErrorResponse,
                        err.response.json(),
                    )
                    logger.error(
                        "Refresh token error '%s': %s",
                        response_error.error,
                        response_error.error_description,
                    )
                else:
                    logger.error(err)

            except MissingScopesError as e:
                logger.error(e)
                self._refresh_daemon_error = True

            # Update the refresh wait time from the newly received access token.
            wait_time = self._get_token_refresh_wait_time()

        logger.debug("[Refresh token] The daemon has stopped.")
        self.has_refresh_daemon_stopped = True

    def start_token_refresh_daemon(self: Self) -> None:
        """Start the token refresh daemon thread."""
        logger.debug("Starting the refresh daemon...")
        refresh_thread = threading.Thread(
            target=self._refresh_token_daemon, daemon=True
        )
        refresh_thread.start()

    def stop_token_refresh_daemon(self: Self) -> None:
        """Stop the token refresh daemon thread."""
        logger.debug("Stopping the refresh daemon...")
        self._stop_refresh_daemon = True
