from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass as pd_dataclass


@pd_dataclass
class DeviceAuthorizationResponse:
    """Represents a Keycloak device authorization endpoint response.
    Refer to the `RFC 8628 related section <https://datatracker.ietf.org/\
    doc/html/rfc8628#section-3.2>`__
    for more information.
    """

    device_code: str
    """The device verification code."""
    user_code: str
    """The end-user verification code."""
    verification_uri: str
    """The end-user verification URI on the authorization server."""
    verification_uri_complete: str
    """A verification URI that includes the "user_code",
    which is designed for non-textual transmission."""
    expires_in: int
    """The lifetime in seconds of the "device_code" and "user_code"."""
    interval: int
    """
    The minimum amount of time in seconds that the client SHOULD wait
    between polling requests to the token endpoint.
    """


@pd_dataclass
class TokenErrorResponse:
    """Represents a Keycloak token endpoint error response."""

    error: str
    """
    A single ASCII error code from the following:
    ``invalid_request``, ``invalid_client``, ``invalid_grant``,
    ``unauthorized_client``, ``unsupported_grant_type``
    (OAuth 2.0 base codes) and ``authorization_pending``, ``slow_down``,
    ``access_denied`` and ``expired_token``
    (additional codes specific to the OAuth 2.0 Device Authorization Grant).
    For details about theses codes, please refer to the
    `RFC 6749 <https://datatracker.ietf.org/doc/html/rfc6749#section-5.2>`__
    and the `RFC 8628 <https://datatracker.ietf.org/\
    doc/html/rfc8628#section-3.2>`__ related sections.
    """
    error_description: str
    """
    Human-readable ASCII text providing additional information,
    used to assist the client developer in understanding the error that
    occurred.
    """


@pd_dataclass
class TokenResponse:
    """Represents a Keycloak token endpoint response.
    Refer to the `RFC 6749 related section <https://datatracker.ietf.org/\
    doc/html/rfc6749#section-5.2>`__
    for more information.
    """

    access_token: str
    """The access token issued by the authorization server for the scopes
    that were requested."""
    expires_in: int
    """The lifetime in seconds of the access token."""
    refresh_expires_in: int
    """The lifetime in seconds of the refresh token."""
    refresh_token: str
    """The refresh token, which can be used to obtain new access tokens
    using the same authorization grant."""
    token_type: str
    """The type of the token issued.
    For the OAuth 2.0 Device Authorization Grant, it is always ``Bearer``."""
    session_state: str
    """State of the session associated with the access token."""
    scope: str
    """Lists the scopes in which the access token is valid for."""


@pd_dataclass
class AuthorizationError:
    """Represents a datawebnode server authorization error.
    This error occurs when the datawebnode server fails to authenticate the
    user (e.g. an invalid access token was used).
    """

    error_name: str
    """Error name."""
    error_code: str
    """Error code."""


@pd_dataclass(order=True)
class VerificationResult:
    """Represents the result of a file checksum verification."""

    filename: str
    """Filename of the verified file."""
    is_valid: bool
    """Indicates whether the checksum is valid or not for the verified file."""
    message: str
    """Message with information about the status of the verification."""


class RemoteFile(BaseModel):
    """Represents metadata associated to remote files."""

    name: str
    """Filename of the file."""
    display_path: str = Field(..., alias="displayPath")
    """Relative path of the file."""
    mtime: str
    """Last modification date of the file."""
    size: int
    """Size of the file."""


class FileType(str, Enum):
    """Represent the types of files."""

    FILE = "FILE"
    CHECKSUM = "CHECKSUM"


class DownloadStatus(str, Enum):
    """Represent the status of downloaded files."""

    ERROR = "ERROR"
    SKIPPED = "SKIPPED"
    SUCCESS = "SUCCESS"


@dataclass(frozen=True)
class LocalFile:
    """This dataclass holds metadata representing a file before it is downloaded."""

    filename: str
    """Filename of the downloaded file."""
    file_type: FileType
    """Type of the downloaded file."""
    path: Path
    """Path were the file will be downloaded to."""
    is_partially_downloaded: bool
    """True if the path is prefixed by ``PARTIAL_DOWNLOAD_SUFFIX``, which means the download of this file was not finalized and
    false otherwise."""


@dataclass(frozen=True)
class DownloadResult:
    """This dataclass holds metadata representing a file after it is downloaded."""

    filename: str
    """Filename of the downloaded file."""
    file_type: FileType
    """Type of the downloaded file."""
    status: DownloadStatus
    """Status of the downloaded file."""
    message: str
    """Message to accompany the status."""


"""Custom type representing a map where an URL (key) is associated to its corresponding LocalFile object (value)."""
LocalFiles = dict[str, LocalFile]

"""Custom type representing a map where an URL (key) is associated to
its corresponding DownloadResult object (value)."""
DownloadResults = dict[str, DownloadResult]
