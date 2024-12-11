import dataclasses
import datetime
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, TypeVar

import requests
from packaging.version import InvalidVersion, Version
from pydantic import TypeAdapter, ValidationError

from cnrgh_dl import config
from cnrgh_dl.download.url import Url
from cnrgh_dl.exceptions import MissingScopesError
from cnrgh_dl.logger import Logger
from cnrgh_dl.models import DownloadResults

logger = Logger.get_instance()
"""Module logger instance."""

T = TypeVar("T")
"""Generic type."""


def check_output_directory(output_dir: Path) -> Path:
    """Check that the given output directory is valid.
    If any exception related to this directory is encountered, the client will exit.

    :param output_dir: Directory where downloaded files will be stored.
    :raises SystemExit: The given path is invalid.
    :return: The path to the output directory, resolved and tilde expanded.
    """
    try:
        output_dir = output_dir.expanduser().resolve(strict=True)
    except FileNotFoundError as err:
        msg = "Error: output path does not exists."
        raise SystemExit(
            msg,
        ) from err
    except RuntimeError as err:
        msg = "Error: an infinite loop was encountered when trying to resolve the output path."
        raise SystemExit(
            msg,
        ) from err
    if not output_dir.is_dir():
        msg = "Error: output path is not a directory."
        raise SystemExit(
            msg,
        )
    return output_dir


def read_urls_from_file(path: Path) -> set[str]:
    """Reads a list of URLs from a file.

    :param path: Path of the file to read content from.
    :raises SystemExit: If the given path does not exist or
        does not point to a file.
    :return: The list of URLs reads.
    """
    if not path.is_file():
        msg = f"{path} does not exists or is not a file."
        raise SystemExit(msg)

    urls: set[str] = set()
    with Path.open(path) as f:
        for line in f:
            url = line.rstrip("\n")

            is_valid, _ = Url.validate(url)
            if is_valid:
                urls.add(url)

    return set(urls)


def get_urls_from_stdin() -> set[str]:
    """Prints to the stdin a menu permitting the user to enter the URLs of
    files to download.

    :raises SystemExit: The user choose to quit the program typing ``q`` / ``quit``.
    :return: A list of URLs of files to download entered by the user.
    """
    logger.info("Paste one or multiple links to download below.")
    logger.info("Type 'l' or 'list' to display the file selection.")
    logger.info("Type 'c' or 'clear' to clear the file selection.")
    logger.info(
        "Type 'v' or 'validate' to start the download of the file selection.",
    )
    logger.info("Type 'q' or 'quit' to quit.")

    urls: set[str] = set()

    for line in sys.stdin:
        user_input = line.rstrip()
        if user_input.lower() in ["validate", "v"]:
            break

        if user_input.lower() in ["quit", "q"]:
            logger.info("Exiting.")
            raise SystemExit(0)

        if user_input.lower() in ["list", "l"]:
            for url in urls:
                logger.info(url)
            logger.info("Total: %s file(s) in queue.", len(urls))
        elif user_input.lower() in ["clear", "c"]:
            urls.clear()
            logger.info("File selection cleared.")
        else:
            is_valid, _ = Url.validate(user_input)
            if is_valid:
                urls.add(user_input)

    return urls


def safe_parse_obj_as(obj_type: type[T], obj: object) -> T:
    """Parses safely an object as a pydantic dataclass.

    :param obj_type: Type of the pydantic dataclass.
    :param obj: Object to convert.
    :raises SystemExit: If the object can't be converted.
    :return: The converted object.
    """
    try:
        return TypeAdapter(obj_type).validate_python(obj)
    except ValidationError as err:
        msg = (
            f"Can't parse the JSON object as a {obj_type.__name__} "
            f"instance: it has missing properties. {err}"
        )
        raise SystemExit(
            msg,
        ) from err


def hash_access_token(access_token: str) -> str:
    """Utility function to return the checksum of an access token.
    An access token is large, and when debugging comparing their checksums
    is easier.

    :param access_token: The access token to hash.
    :return: The hexadecimal digested checksum of the access token.
    """
    return hashlib.md5(access_token.encode("utf-8")).hexdigest()


def remove_keys_from(
    target: dict[str, Any],
    origin: dict[str, Any],
) -> dict[str, Any]:
    keys_to_remove = set()
    for key in target:
        if key in origin:
            keys_to_remove.add(key)

    for key in keys_to_remove:
        del target[key]

    return target


def check_for_update() -> tuple[bool, str]:
    """Print a message if a newer version of the package is available on the PyPI repository.
    :returns: A tuple containing in first position a boolean telling if a newer version of the package is available,
    and in second position a code indicating a success or detailing an error.
    This tuple is only returned for testing purposes.
    """
    if not config.PYPI_REPOSITORY:
        logger.debug("No PYPI repository configured, skipping update check.")
        return False, "update_check_skipped"

    repo_url = f"https://{config.PYPI_REPOSITORY}/pypi/cnrgh-dl/json"
    logger.debug("Current version of cnrgh-dl is %s.", config.APP_VERSION)

    try:
        response = requests.get(repo_url, timeout=config.REQUESTS_TIMEOUT)
        response.raise_for_status()
        data = response.json()

        latest_version = data["info"]["version"]
        logger.debug("Latest version of cnrgh-dl is %s.", latest_version)

        local_v = Version(config.APP_VERSION)
        remote_v = Version(latest_version)

    except requests.RequestException as e:
        logger.debug("Could not obtain latest version of package: %s", e)
        return False, "request_error"

    except KeyError:
        logger.debug(
            "Could not obtain latest version of package: 'version' key not found in JSON."
        )
        return False, "no_version_in_response"

    except InvalidVersion as e:
        logger.debug("Could not parse a version string: %s", e)
        return False, "invalid_version_string"

    if remote_v > local_v:
        logger.info(
            "A newer version of cnrgh-dl is available. Please update to the latest version: %s "
            "(installed version: %s).",
            remote_v,
            local_v,
        )
        logger.info(
            "Refer to the following page for update instructions: "
            "https://www.cnrgh.fr/data-userdoc/download_with_client/#mise-a-jour."
        )
        return True, "newer_version_available"

    logger.debug("Latest version of cnrgh-dl is installed.")
    return False, "latest_version_installed"


def write_json_report(report_path: Path, dl_results: DownloadResults) -> bool:
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")  # noqa: DTZ005
        report_path = Path(report_path / f"cnrgh_dl_report_{timestamp}.json")
        with report_path.open(mode="w+", encoding="utf-8") as f:
            # Convert DownloadResult dataclasses to dicts.
            json_results = {
                k: dataclasses.asdict(v) for k, v in dl_results.items()
            }
            json.dump(json_results, f, ensure_ascii=False, indent=4)
            logger.info("JSON report written to %s", report_path)

        success = True
    except OSError as e:
        logger.error(
            "An error occurred while trying to write the JSON report. %s", e
        )
        success = False

    return success


def verify_scopes(requested_scopes: str, granted_scopes: str) -> None:
    """Verify that the authorization server granted all the requested scopes.
    This ensures that the access token has all the scopes required by the client.

    :param requested_scopes: A string containing the requested scopes, space-delimited.
    :param granted_scopes: A string containing the scopes granted by the authorization server, space-delimited.
    :raises MissingScopesError: Some requested scopes are missing from the scopes granted by the authorization server.
    """
    requested_scopes_set = set(requested_scopes.split())
    granted_scopes_set = set(granted_scopes.split())

    if requested_scopes_set.issubset(granted_scopes_set):
        logger.debug(
            "All requested scopes have been granted: %s.", requested_scopes
        )
    else:
        missing_scopes = requested_scopes_set - granted_scopes_set
        raise MissingScopesError(missing_scopes)
