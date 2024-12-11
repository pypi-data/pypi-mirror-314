from importlib.metadata import metadata, version

from environs import Env
from marshmallow.validate import OneOf
from platformdirs import user_log_path

env = Env()
"""Environment variables reader."""
env.read_env()

APP_NAME = __package__
APP_VERSION = version(__package__)
APP_AUTHOR = metadata(__package__)["Author"]
REQUESTS_TIMEOUT = 60
PARTIAL_DOWNLOAD_SUFFIX = ".part"
"""
Suffix indicating that a file has been partially downloaded.
"""

REQUESTED_ACCESS_SCOPE = "openid groups profile audience offline_access"
"""
Access scope requested by cnrgh-dl (OpenID Connect client) to Keycloak (authorization server).
Keycloak will issue an access token with the requested scope.
The scope 'openid' is mandatory to access the userinfo endpoint.
'profile' and 'groups' scopes add user profile and group data to the userinfo response.
The 'audience' scope specifies the intended recipient of the access token,
ensuring it can only be used by either Keycloak or datawebnode.
The 'offline_access' scope asks for an offline refresh token,
which is not linked to the SSO session unlike a standard refresh token.
"""

LOG_SAVE_FILE = (
    user_log_path(APP_NAME, APP_AUTHOR, APP_VERSION, ensure_exists=True)
    / f"{APP_NAME}.log"
)
"""
Path to the file where the application logs are written, located in the user log directory.
"""

LOG_LEVEL = env.log_level("CNRGHDL_LOG_LEVEL", "INFO")
"""
Log level of the application read from the CNRGHDL_LOG_LEVEL environment variable.
If CNRGHDL_LOG_LEVEL is not set, it is equal to ``INFO`` (production value).
"""

KEYCLOAK_SERVER_ROOT_URL = env.url(
    "CNRGHDL_KEYCLOAK_SERVER_ROOT_URL",
    "https://keycloak.ibfj-evry.fr/",
).geturl()
"""
Keycloak server root URL read from the ``CNRGHDL_KEYCLOAK_SERVER_ROOT_URL``
environment variable.
If ``CNRGHDL_KEYCLOAK_SERVER_ROOT_URL`` is not set,
it is equal to ``https://keycloak.ibfj-evry.fr/`` (production value).
"""

KEYCLOAK_REALM_ID = env.str(
    "CNRGHDL_KEYCLOAK_REALM_ID", "IBFJ-EVRY-OU-CollabExt"
)
"""
Keycloak realm identifier read from the ``CNRGHDL_KEYCLOAK_REALM_ID``
environment variable.
If ``CNRGHDL_KEYCLOAK_SERVER_ROOT_URL`` is not set,
it is equal to ``IBFJ-EVRY-OU-CollabExt`` (production value).
"""

KEYCLOAK_CLIENT_ID = env.str("CNRGHDL_KEYCLOAK_CLIENT_ID", "cnrgh-dl")
"""
Keycloak client identifier read from the ``CNRGHDL_KEYCLOAK_CLIENT_ID``
environment variable.
If ``CNRGHDL_KEYCLOAK_CLIENT_ID`` is not set,
it is equal to ``data-web-node-dev`` (production value).
"""

DATAWEBNODE_API_BASE_PATH = env.url(
    "CNRGHDL_DATAWEBNODE_API_BASE_PATH",
    "https://www.cnrgh.fr/data2/api/",
).geturl()
"""
``datawebnode`` server download endpoint URL read from the
``CNRGHDL_DATAWEBNODE_API_BASE_PATH`` environment variable.
This variable is used to define the API base path of the server.
If ``CNRGHDL_DATAWEBNODE_API_BASE_PATH`` is not set, it is equal to
``https://www.cnrgh.fr/data2/api/`` (production value).
"""

DATAWEBNODE_DOWNLOAD_ENDPOINT = f"{DATAWEBNODE_API_BASE_PATH}download/"
"""
``datawebnode`` server download endpoint URL deduced from the ``CNRGHDL_DATAWEBNODE_API_BASE_PATH`` environment variable.
This variable is used to ensure that only files available on the ``datawebnode`` server can be downloaded with this client.
"""

DATAWEBNODE_PROJECT_FILES_ENDPOINT = f"{DATAWEBNODE_API_BASE_PATH}project/"
"""
``datawebnode`` server download endpoint URL deduced from the ``CNRGHDL_DATAWEBNODE_API_BASE_PATH`` environment variable.
This variable is used to request project files metadata to the server.
"""

ISSUER = f"{KEYCLOAK_SERVER_ROOT_URL}realms/{KEYCLOAK_REALM_ID}"
"""Keycloak issuer URL deduced from the ``KEYCLOAK_SERVER_ROOT_URL`` and
the ``KEYCLOAK_REALM_ID`` values."""

KEYCLOAK_DEVICE_AUTH_ENDPOINT = f"{ISSUER}/protocol/openid-connect/auth/device"
"""
Keycloak device authentication endpoint deduced from the ``ISSUER`` value.
Refer to the `device endpoint documentation <https://www.keycloak.org/\
docs/latest/securing_apps/index.html#device-authorization-endpoint>`__
for more information.
"""

KEYCLOAK_TOKEN_ENDPOINT = f"{ISSUER}/protocol/openid-connect/token"
"""
Keycloak token endpoint deduced from the ``ISSUER`` value.
Refer to the `token endpoint documentation <https://www.keycloak.org/\
docs/latest/securing_apps/index.html#token-endpoint>`__
for more information.
"""

KEYCLOAK_USER_INFO_ENDPOINT = f"{ISSUER}/protocol/openid-connect/userinfo"
"""
Keycloak userinfo endpoint deduced from the ``ISSUER`` value.
Refer to the `userinfo endpoint documentation <https://www.keycloak.org/\
docs/latest/securing_apps/index.html#userinfo-endpoint>`__
for more information.
"""

KEYCLOAK_DEVICE_LOGIN_URI = f"{ISSUER}/device"
"""
URI that the user should visit in order to complete the authentication process.
It is deduced from the ``ISSUER`` value.
"""

PYPI_REPOSITORY = env.str(
    "CNRGHDL_PYPI_REPOSITORY",
    "pypi.org",
    validate=OneOf(["pypi.org", "test.pypi.org", ""]),
)
"""
PyPI repository hostname to use to check for a package update,
read from the ``CNRGHDL_PYPI_REPOSITORY`` environment variable.
This can be set to ``test.pypi.org`` in a development environment,
or to ``pypi.org`` in a production environment.
If ``CNRGHDL_PYPI_REPOSITORY`` is set to an empty string, the update check will be skipped.
If ``CNRGHDL_PYPI_REPOSITORY`` is not set, it is equal to ``pypi.org`` (production value).
"""
