import shutil
from pathlib import Path

import requests
import urllib3.exceptions
from tqdm import tqdm
from typing_extensions import Self

from cnrgh_dl import config
from cnrgh_dl.auth.token_manager import TokenManager
from cnrgh_dl.download.url import Url
from cnrgh_dl.exceptions import PrematureDownloadTerminationError
from cnrgh_dl.logger import Logger
from cnrgh_dl.models import (
    DownloadResult,
    DownloadResults,
    DownloadStatus,
    FileType,
    LocalFile,
    RemoteFile,
)
from cnrgh_dl.utils import hash_access_token, safe_parse_obj_as

logger = Logger.get_instance()
"""Module logger instance."""


class Downloader:
    """Handle the downloads."""

    _token_manager: TokenManager
    """A token manager instance to obtain a valid access token to
    include in each request made to the datawebnode server."""
    _output_dir: Path
    """Output directory where downloaded files are stored."""

    def __init__(
        self: Self,
        token_manager: TokenManager,
        output_dir: Path,
    ) -> None:
        """Initialize a downloader with a token manager and
        an output directory to store files.
        """
        self._token_manager = token_manager
        self._output_dir = output_dir

    def _get_md5_from_project(self: Self, project_name: str) -> set[str]:
        """By using the project API endpoint with a project name,
        the server returns a JSON list of all the files contained within this project directory.
        We then only keep files with an ``.md5`` extension.

        :param project_name: The name of the project for which we want to retrieve the
            list of MD5 checksum file URLs.
        :return: A set of MD5 checksum file URLs present inside the directory.
        """
        retrieved_md5s: set[str] = set()

        try:
            response = requests.get(
                config.DATAWEBNODE_PROJECT_FILES_ENDPOINT + project_name,
                headers={
                    "Authorization": f"Bearer {self._token_manager.token_response.access_token}",
                },
                timeout=config.REQUESTS_TIMEOUT,
            )
            response.raise_for_status()
            json = response.json()

            files = safe_parse_obj_as(list[RemoteFile], json)

            for file in files:
                if Url.get_path_extension(file.display_path) == ".md5":
                    retrieved_md5s.add(file.display_path)

        except requests.exceptions.RequestException:
            logger.error(
                "Could not download a list of files for "
                "the '%s' project. As a result, checksum for "
                "files from this directory won't be downloaded.",
                project_name,
            )
        return retrieved_md5s

    def fetch_additional_checksums(
        self: Self,
        urls: set[str],
    ) -> dict[str, LocalFile]:
        """For a given set of file URLs, retrieve their checksums from the datawebnode server if they exist.

        :param urls: A set of URLs for which we want to retrieve their checksums.
        :return: A queue of the found checksums. It is a dict containing as keys URLs of files to download and
            as values LocalFile instances containing metadata about the file that will be downloaded.
        """
        additional_checksum_urls: dict[str, LocalFile] = {}
        relative_file_paths: set[str] = set()
        project_names: set[str] = set()

        # 1. Obtain a set of project names.
        for url in urls:
            relative_file_path = url[
                len(config.DATAWEBNODE_DOWNLOAD_ENDPOINT) :
            ]
            relative_file_paths.add(relative_file_path)
            project_name = relative_file_path.split("/")[0]
            project_names.add(project_name)

        # 2. From the API, retrieve for each project
        # the list of files it contains and add only the MD5 files to a set.
        md5s_available: set[str] = set()
        for url in project_names:
            md5s_available.update(self._get_md5_from_project(url))

        # 3. If a file in the download list matches a MD5,
        # we add the MD5 to the download list.
        for relative_file_path in relative_file_paths:
            checksum_path = f"{relative_file_path}.md5"
            if checksum_path in md5s_available:
                filename = checksum_path.rsplit("/")[-1]
                filepath = Path(self._output_dir / filename)
                is_partially_downloaded = False

                additional_checksum_urls[
                    config.DATAWEBNODE_DOWNLOAD_ENDPOINT + checksum_path
                ] = LocalFile(
                    filename,
                    FileType.CHECKSUM,
                    filepath,
                    is_partially_downloaded,
                )

        return additional_checksum_urls

    def _download(
        self: Self,
        url: str,
        local_file: LocalFile,
        *,
        force_download: bool,
    ) -> None:
        """Download a file from the datawebnode server.
        This function can also continue a partial download by sending a Range header to the server
        if ``local_file.is_partially_downloaded`` is ``True``.

        :param url: The URL of the file to download,
            hosted on the datawebnode server.
        :param local_file: A LocalFile instance containing metadata about the file that will be downloaded.
        :param force_download: Flag to force the download of files.
        :raises requests.exceptions.RequestException:
            An error occurred while requesting the file.
        :raises requests.RequestException:
            An error occurred while handling the download request.
        :raises urllib3.exceptions.ReadTimeoutError:
            The network connection was lost while receiving a file.
        :raises PrematureDownloadTerminationError:
            The download could not fully finish because the server went down.
        :raises FileNotFoundError:
            The file was moved or deleted during the download.
        :raises Exception:
            An exception other than those listed above has been raised.
        """
        logger.debug(
            "Download using access token = %s.",
            hash_access_token(self._token_manager.token_response.access_token),
        )
        partial_save_path = local_file.path.with_suffix(
            local_file.path.suffix + config.PARTIAL_DOWNLOAD_SUFFIX,
        )

        headers = {
            "Authorization": f"Bearer {self._token_manager.token_response.access_token}",
        }
        open_mode = "wb"

        if local_file.is_partially_downloaded:
            if force_download:
                partial_save_path.unlink(missing_ok=True)
            else:
                downloaded_size = partial_save_path.stat().st_size
                headers["Range"] = f"bytes={downloaded_size}-"
                open_mode = "ab"

        response = requests.get(
            url,
            stream=True,
            headers=headers,
            timeout=config.REQUESTS_TIMEOUT,
        )
        response.raise_for_status()

        file_size = int(response.headers.get("Content-Length", 0))

        desc = (
            f"{local_file.filename} (unknown total file size)"
            if file_size == 0
            else f"{local_file.filename}"
        )

        with (
            tqdm.wrapattr(
                response.raw,
                "read",
                total=file_size,
                unit="B",
                unit_scale=True,
                miniters=1,
                desc=desc,
                leave=False,
            ) as r_raw,
            Path.open(partial_save_path, open_mode) as f,
        ):
            shutil.copyfileobj(r_raw, f, length=16 * 1024 * 1024)

        # If the server goes down during a download,
        # raise an exception because the file has not been fully downloaded.
        if partial_save_path.stat().st_size < file_size:
            raise PrematureDownloadTerminationError

        partial_save_path.rename(local_file.path)

    def download_queue(
        self: Self,
        queue: dict[str, LocalFile],
        *,
        force_download: bool,
    ) -> DownloadResults:
        """Download a queue of URLs.

        :param queue: A dict containing as keys URLs of files to download and
            as values LocalFile instances containing metadata about the file that will be downloaded.
        :param force_download: Flag to force the download of files.
        :return: A dict containing as keys files URLs and as values error messages.
        """
        dl_results = {}

        for url in sorted(queue.keys()):
            local_file = queue[url]
            is_file_download_complete = (
                local_file.path.is_file()
                and not local_file.is_partially_downloaded
            )

            if not force_download and is_file_download_complete:
                dl_results.update(
                    {
                        url: DownloadResult(
                            local_file.filename,
                            local_file.file_type,
                            DownloadStatus.SKIPPED,
                            "File already exists in the output directory.",
                        ),
                    },
                )
                logger.warning(
                    "Skipping download of file %s as it already exists in the output directory.",
                    str(local_file.filename),
                )
                continue

            if self._token_manager.has_refresh_daemon_stopped:
                dl_results.update(
                    {
                        url: DownloadResult(
                            local_file.filename,
                            local_file.file_type,
                            DownloadStatus.ERROR,
                            "Could not acquire an access token to download the file.",
                        ),
                    },
                )
                logger.error(
                    "File %s could not be downloaded as there was an error trying to acquire an access token.",
                    str(local_file.filename),
                )
                continue

            try:
                logger.info("Starting download of %s.", queue[url].filename)
                self._download(url, queue[url], force_download=force_download)
                logger.info("%s successfully downloaded.", queue[url].filename)
                dl_results.update(
                    {
                        url: DownloadResult(
                            local_file.filename,
                            local_file.file_type,
                            DownloadStatus.SUCCESS,
                            "File successfully downloaded.",
                        ),
                    },
                )

            except requests.RequestException as err:
                dl_results.update(
                    {
                        url: DownloadResult(
                            local_file.filename,
                            local_file.file_type,
                            DownloadStatus.ERROR,
                            "An error occurred while handling the download request.",
                        ),
                    },
                )
                logger.error(err)
            except urllib3.exceptions.ReadTimeoutError as err:
                dl_results.update(
                    {
                        url: DownloadResult(
                            local_file.filename,
                            local_file.file_type,
                            DownloadStatus.ERROR,
                            "Read timed out.",
                        ),
                    },
                )
                logger.error(err)
            except PrematureDownloadTerminationError as err:
                dl_results.update(
                    {
                        url: DownloadResult(
                            local_file.filename,
                            local_file.file_type,
                            DownloadStatus.ERROR,
                            "Download could not fully finish.",
                        ),
                    },
                )
                logger.error(err)
            except FileNotFoundError as err:
                dl_results.update(
                    {
                        url: DownloadResult(
                            local_file.filename,
                            local_file.file_type,
                            DownloadStatus.ERROR,
                            "File was moved or deleted during the download.",
                        ),
                    },
                )
                logger.error(err)
            except Exception as err:  # noqa: BLE001
                dl_results.update(
                    {
                        url: DownloadResult(
                            local_file.filename,
                            local_file.file_type,
                            DownloadStatus.ERROR,
                            "An error occurred.",
                        ),
                    },
                )
                logger.error(err)

        return dl_results
