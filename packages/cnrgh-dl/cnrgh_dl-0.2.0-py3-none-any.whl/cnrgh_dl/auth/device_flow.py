import time

import requests
from requests import Response

from cnrgh_dl import config
from cnrgh_dl.config import REQUESTED_ACCESS_SCOPE
from cnrgh_dl.exceptions import MissingScopesError
from cnrgh_dl.logger import Logger
from cnrgh_dl.models import (
    DeviceAuthorizationResponse,
    TokenErrorResponse,
    TokenResponse,
)
from cnrgh_dl.utils import safe_parse_obj_as, verify_scopes

logger = Logger.get_instance()
"""Module logger instance."""


class DeviceFlow:
    """Implementation of the OAuth 2.0 Device Authorization Grant
    (formerly known as the Device Flow) to obtain an access token from
    the Keycloak server.

    If any error occurs while trying to obtain an access token,
    the client will exit.

    See the `RFC 8628 <https://datatracker.ietf.org/doc/html/rfc8628>`__
    for detailed explanations.
    """

    @staticmethod
    def _get_device_authorization() -> DeviceAuthorizationResponse:
        """Corresponds to the first step of the OAuth 2.0 Device Authorization
        Grant: obtain a device authorization code from the Keycloak server.

        In this step, we obtain (among other data) from the Keycloak server
        a user code, a verification URI and a device code which are
        needed to complete the second step of the
        OAuth 2.0 Device Authorization Grant.

        If any error occurs while trying to obtain a device code,
        the client will exit.

        For more information about this step, please refer to the
        `authorization request documentation <https://www.oauth.com/\
        oauth2-servers/device-flow/authorization-request/>`__.

        :raises SystemExit: An exception occurred while handling the device authorization request.
        :return: A DeviceAuthorizationResponse dataclass,
            containing attributes needed for the second step of the
            OAuth 2.0 Device Authorization Grant.
        """
        params: dict[str, str] = {
            "client_id": config.KEYCLOAK_CLIENT_ID,
            "scope": config.REQUESTED_ACCESS_SCOPE,
        }

        try:
            response: Response = requests.post(
                config.KEYCLOAK_DEVICE_AUTH_ENDPOINT,
                data=params,
                timeout=config.REQUESTS_TIMEOUT,
            )
            response.raise_for_status()
            return safe_parse_obj_as(
                DeviceAuthorizationResponse, response.json()
            )

        except requests.exceptions.RequestException as err:
            raise SystemExit(err.__str__()) from err

    @staticmethod
    def _get_token(
        device_authorization_response: DeviceAuthorizationResponse,
    ) -> TokenResponse:
        """Corresponds to the second step of the OAuth 2.0 Device Authorization
        Grant. It instructs the user to visit the Keycloak verification URI
        and enter its user code.

        While the user authorizes the client to access his account,
        this function polls the Keycloak server waiting for the end of the
        authorization process.

        If any error occurs while trying to obtain an access token,
        the client will exit.

        For more information about this step, please refer to the
        `token request documentation <https://www.oauth.com/\
        oauth2-servers/device-flow/token-request/>`__.

        :param device_authorization_response: A DeviceAuthorizationResponse
            dataclass, obtained after successfully completing the
            first step of the OAuth 2.0 Device Authorization Grant.
        :raises SystemExit: An exception occurred while handling the token request.
        :return: A TokenResponse dataclass, containing among others attributes
            an access and a refresh token.
        """
        params: dict[str, str] = {
            "client_id": config.KEYCLOAK_CLIENT_ID,
            "device_code": device_authorization_response.device_code,
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
        }

        verification_uri = device_authorization_response.verification_uri
        # sometimes Keycloak does not put the device login URI
        # into the response.
        if not verification_uri:
            verification_uri = config.KEYCLOAK_DEVICE_LOGIN_URI

        polling_interval: int = device_authorization_response.interval
        message_interval: int = 15
        last_message_time: float = 0
        start_time: float = time.time()

        while True:
            try:
                response: Response = requests.post(
                    config.KEYCLOAK_TOKEN_ENDPOINT,
                    data=params,
                    timeout=config.REQUESTS_TIMEOUT,
                )

                if response.ok:
                    return safe_parse_obj_as(TokenResponse, response.json())

                error_response: TokenErrorResponse = safe_parse_obj_as(
                    TokenErrorResponse,
                    response.json(),
                )

                if error_response.error == "slow_down":
                    polling_interval += (
                        5  # Add 5 seconds to the polling interval until
                    )
                    # the server does not return the same error.
                elif error_response.error != "authorization_pending":
                    msg = f"{error_response.error}: {error_response.error_description}"
                    raise SystemExit(
                        msg,
                    )

            except requests.exceptions.RequestException as err:
                raise SystemExit(err.__str__()) from err

            current_time: float = time.time()
            elapsed_time: float = current_time - start_time

            remaining_lifespan = (
                device_authorization_response.expires_in
                - round(
                    elapsed_time,
                )
            )

            if current_time - last_message_time >= message_interval:
                logger.info(
                    "To login, please open %s in a web browser and "
                    "enter the following code : %s "
                    "(expiring in %s seconds).",
                    verification_uri,
                    device_authorization_response.user_code,
                    remaining_lifespan,
                )
                last_message_time = current_time

            logger.debug(
                "Will try to poll the Keycloak server again in %s seconds.",
                polling_interval,
            )
            time.sleep(polling_interval)

    @staticmethod
    def start() -> TokenResponse:
        """Start the entirety of the OAuth 2.0 Device Authorization Grant flow,
        to obtain an access and a refresh token at its end.

        If any error occurs while trying to obtain an access token,
        the client will exit.

        :raises SystemExit: An exception occurred while handling the device authorization and token requests or
            the generated access token does not contain all the requested scopes.
        :return: A TokenResponse dataclass, containing among others attributes
            an access and a refresh token.
        """
        logger.debug("OAuth 2.0 Device Authorization Grant flow started.")
        device_authorization_response: DeviceAuthorizationResponse = (
            DeviceFlow._get_device_authorization()
        )
        logger.debug("Device Authorization Grant obtained from Keycloak.")
        token_response = DeviceFlow._get_token(device_authorization_response)
        logger.debug(
            "Access and refresh tokens successfully obtained from Keycloak.",
        )
        # Ensure that the server granted all the required scopes.
        try:
            verify_scopes(REQUESTED_ACCESS_SCOPE, token_response.scope)
        except MissingScopesError as e:
            raise SystemExit(e) from e

        return token_response
