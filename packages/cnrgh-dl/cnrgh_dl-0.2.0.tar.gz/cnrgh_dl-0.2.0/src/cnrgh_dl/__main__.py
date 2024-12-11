import dataclasses
import os
import sys
from enum import Enum

from cnrgh_dl import config
from cnrgh_dl.args import get_args
from cnrgh_dl.auth.token_manager import TokenManager
from cnrgh_dl.download.downloader import Downloader
from cnrgh_dl.download.integrity import Integrity
from cnrgh_dl.download.queue import find_partial_downloads, init_queue
from cnrgh_dl.exit import CustomSigIntHandler
from cnrgh_dl.logger import Logger
from cnrgh_dl.models import (
    DownloadResult,
    DownloadResults,
    DownloadStatus,
    LocalFiles,
)
from cnrgh_dl.utils import (
    check_for_update,
    check_output_directory,
    get_urls_from_stdin,
    read_urls_from_file,
    remove_keys_from,
    write_json_report,
)

logger = Logger.get_instance()
"""Module logger instance."""


def start_download(
    downloader: Downloader,
    file_queue: LocalFiles,
    checksum_queue: LocalFiles,
    *,
    force_download: bool,
) -> DownloadResults:
    """Start the download of files and then checksums.

    :param downloader: A download instance.
    :param file_queue: Queue of files to download.
    :param checksum_queue: Queue of checksums to download.
    :param force_download: Flag to force the download of files.
    :return: A dict containing download results.
    """
    dl_results = {}

    if len(file_queue) > 0:
        logger.info("==============================")
        logger.info("Starting the download of files")
        logger.info("==============================")
        dl_results.update(
            downloader.download_queue(
                file_queue,
                force_download=force_download,
            ),
        )

    if len(checksum_queue) > 0:
        logger.info("==================================")
        logger.info("Starting the download of checksums")
        logger.info("==================================")
        dl_results.update(
            downloader.download_queue(
                checksum_queue,
                force_download=force_download,
            ),
        )

    return dl_results


def start_integrity_check(
    file_queue: LocalFiles,
    checksum_queue: LocalFiles,
    dl_results: DownloadResults,
) -> None:
    """Start the integrity check of downloaded files by computing their checksums and
    comparing them with the downloaded ones if they exist.

    :param file_queue: Queue of files to download.
    :param checksum_queue: Queue of checksums to download.
    :param dl_results: Dict containing download results.
    """
    logger.info("===============")
    logger.info("INTEGRITY CHECK")
    logger.info("===============")

    if len(file_queue) == 0:
        logger.warning(
            "Skipped the integrity check: there is no files to check.",
        )
        return

    if len(checksum_queue) == 0:
        logger.warning(
            "Skipped the integrity check: there is no checksums to validate files against.",
        )
        return

    Integrity.check(file_queue, checksum_queue, dl_results)


def start_additional_checksum_download(
    downloader: Downloader,
    file_queue: LocalFiles,
    checksum_queue: LocalFiles,
    *,
    force_download: bool,
) -> DownloadResults:
    """Start the download of additional checksums from the datawebnode server.

    If available on the datawebnode server and if not already downloaded,
    additional checksums will be downloaded in order to verify the maximum of downloaded files.

    :param downloader: A download instance.
    :param file_queue: Queue of files to download.
    :param checksum_queue: Queue of checksums to download.
    :param force_download: Flag to force the download of files.
    :return: A dict containing as keys files URLs and as values error messages.
    """
    dl_results = {}
    # Remove checksums already present in the download queue to not download them again.
    additional_checksum_queue = remove_keys_from(
        downloader.fetch_additional_checksums(set(file_queue.keys())),
        checksum_queue,
    )

    if len(additional_checksum_queue) > 0:
        logger.info(
            "====================================="
            "=====================================",
        )
        logger.info(
            "Starting the download of additional checksums "
            "(for verification purposes).",
        )
        logger.info(
            "====================================="
            "=====================================",
        )
        dl_results.update(
            downloader.download_queue(
                additional_checksum_queue,
                force_download=force_download,
            ),
        )
        checksum_queue.update(additional_checksum_queue)

    return dl_results


def print_download_recap(
    file_queue: LocalFiles,
    checksum_queue: LocalFiles,
    dl_results: DownloadResults,
) -> None:
    """Print a recap after all the files have been downloaded.

    :param file_queue: Queue of files to download.
    :param checksum_queue: Queue of checksums to download.
    :param dl_results: Dict containing download results.
    """
    checksum_filenames = set(checksum_queue.keys())
    filenames = set(file_queue.keys())
    checksum_count = 0
    file_count = 0
    error_count = 0

    for url, result in dl_results.items():
        if result.status == DownloadStatus.ERROR:
            error_count += 1
            continue

        if result.status == DownloadStatus.SUCCESS:
            if url in checksum_filenames:
                checksum_count += 1
            if url in filenames:
                file_count += 1

    logger.info(
        "Downloaded %d of %d file(s), "
        "%d of %d checksum(s) and encountered %d error(s).",
        file_count,
        len(file_queue),
        checksum_count,
        len(checksum_queue),
        error_count,
    )


def print_download_summary(dl_results: DownloadResults) -> None:
    """Print the download summary.

    :param dl_results: Dict containing download results.
    """
    logger.info("================")
    logger.info("DOWNLOAD SUMMARY")

    format_string = ""
    full_tab_width = 0
    columns_margin = 3
    table_lines: list[list[str]] = []
    fields = [field.name for field in dataclasses.fields(DownloadResult)]

    # Create a list containing the lines of the table to print.
    for index, dl_result in enumerate(dl_results.values()):
        table_lines.append([])
        for field in fields:
            field_value = dl_result.__dict__[field]
            if isinstance(field_value, Enum):
                table_lines[index].append(field_value.value)
            else:
                table_lines[index].append(field_value)

    # Transform fields into table headers.
    headers = [field.replace("_", " ") for field in fields]

    # For each table column, we compute its maximum value length (including its header).
    for index in range(len(headers)):
        # Compute the length of all the column values and its header.
        values_length = [len(line[index]) for line in table_lines]
        values_length.append(len(headers[index]))
        # Get the maximum value length.
        width = max(values_length) + columns_margin
        # Create a format string for this column.
        format_string += "{:<" + str(width) + "}"
        full_tab_width += width

    logger.info("=" * full_tab_width)
    logger.info(format_string.format(*headers))
    logger.info("-" * full_tab_width)

    # Print the table lines with the corresponding level.
    for index, dl_result in enumerate(dl_results.values()):
        if dl_result.status is DownloadStatus.ERROR:
            logger.error(format_string.format(*table_lines[index]))
        elif dl_result.status is DownloadStatus.SKIPPED:
            logger.warning(format_string.format(*table_lines[index]))
        else:
            logger.info(format_string.format(*table_lines[index]))

    logger.info("=" * full_tab_width)


def main() -> int:
    """Main function of ``cnrgh-dl``.
    Depending on the presence and the value of the parsed
    command line arguments, it runs the corresponding functions.

    :raises SystemExit: The file download list is empty.
    """
    # On Windows, registering a custom SIGINT handler to ask for user confirmation before exiting
    # results in the message "Terminate batch job (Y/N)" always being prompted.
    # The response to the custom handler will be ignored, and if we choose not to terminate the job by typing 'N',
    # the script will still be unable to resume execution.
    # Therefore, we only register the custom handler for other platforms where it functions correctly.
    if os.name != "nt":
        logger.debug(
            "Custom handler for SIGINT registered to ask for user confirmation before exiting."
        )
        custom_sigint_handler = CustomSigIntHandler()
        custom_sigint_handler.register_custom_handler()

    logger.debug("KEYCLOAK_SERVER_ROOT_URL=%s", config.KEYCLOAK_SERVER_ROOT_URL)
    logger.debug("KEYCLOAK_REALM_ID=%s", config.KEYCLOAK_REALM_ID)
    logger.debug("KEYCLOAK_CLIENT_ID=%s", config.KEYCLOAK_CLIENT_ID)
    logger.debug(
        "DATAWEBNODE_DOWNLOAD_ENDPOINT=%s",
        config.DATAWEBNODE_DOWNLOAD_ENDPOINT,
    )
    logger.debug("Logs are written to: %s", config.LOG_SAVE_FILE)

    check_for_update()

    args = get_args()
    output_dir = check_output_directory(args.outdir)
    dl_results = {}

    token_manager = TokenManager()
    # Start a thread that will periodically refresh
    # the access and refresh tokens.
    token_manager.start_token_refresh_daemon()

    if args.input_file:
        urls = read_urls_from_file(args.input_file)
    else:
        urls = get_urls_from_stdin()

    if len(urls) == 0:
        msg = "Error: empty list of files to download."
        raise SystemExit(msg)

    downloader = Downloader(token_manager, output_dir)

    partially_downloaded_files = find_partial_downloads(urls, output_dir)
    if not args.force_download and len(partially_downloaded_files) > 0:
        logger.warning(
            "Some files in the download queue are already present in the output folder but are incomplete. "
            "Their download will be continued.",
        )

        for file in partially_downloaded_files:
            logger.warning("'%s': incomplete download.", file)

    file_queue, checksum_queue = init_queue(
        urls,
        output_dir,
        partially_downloaded_files,
    )

    dl_results.update(
        start_download(
            downloader,
            file_queue,
            checksum_queue,
            force_download=args.force_download,
        ),
    )

    if not args.no_additional_checksums:
        dl_results.update(
            start_additional_checksum_download(
                downloader,
                file_queue,
                checksum_queue,
                force_download=args.force_download,
            ),
        )

    # All downloads are finished, stop the refresh daemon.
    token_manager.stop_token_refresh_daemon()

    print_download_summary(dl_results)
    print_download_recap(file_queue, checksum_queue, dl_results)

    if not args.no_integrity_check:
        start_integrity_check(file_queue, checksum_queue, dl_results)

    if args.json_report:
        write_json_report(output_dir, dl_results)

    # If one or more downloads encounter an error, we return 0 as the status code.
    # Otherwise, we return 1 because all the files were either successfully downloaded or skipped.
    return not any(
        dl_result.status == DownloadStatus.ERROR
        for dl_result in dl_results.values()
    )


if __name__ == "__main__":
    sys.exit(main())
