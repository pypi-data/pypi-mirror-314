import os
from pathlib import Path

from cnrgh_dl import config
from cnrgh_dl.download.url import Url
from cnrgh_dl.models import FileType, LocalFile, LocalFiles


def find_partial_downloads(urls: set[str], output_dir: Path) -> set[str]:
    """Finds partially downloaded files (suffixed by ``PARTIAL_DOWNLOAD_SUFFIX``) in the output directory.

    :param urls: Set of URLs to download.
    :param output_dir: Output directory where files will be downloaded,
        and where this function should search for partially downloaded files.
    :return: A list of filenames which were partially downloaded (without the ``PARTIAL_DOWNLOAD_SUFFIX`` suffix).
    """
    url_filenames = {Url.get_path_filename(url) for url in urls}

    entries = os.listdir(output_dir)
    partially_downloaded_files = set()

    for entry in entries:
        entry_path = Path(output_dir / entry)

        if entry_path.is_file():
            file_without_part_suffix = entry[
                : -len(config.PARTIAL_DOWNLOAD_SUFFIX)
            ]

            if (
                entry_path.suffix == config.PARTIAL_DOWNLOAD_SUFFIX
                and file_without_part_suffix in url_filenames
            ):
                partially_downloaded_files.add(file_without_part_suffix)

    return partially_downloaded_files


def init_queue(
    urls: set[str],
    output_dir: Path,
    partially_downloaded_files: set[str],
) -> tuple[LocalFiles, LocalFiles]:
    """Initialize the download queue, which contains the files to download.
    The queue is split in two as we want to download checksum separately.

    :param urls: Set of URLs to download.
    :param output_dir: Output directory where files will be downloaded,
    :param partially_downloaded_files: A set of filenames from files that were found to be partially downloaded.
        The filenames should not contain the ``PARTIAL_DOWNLOAD_SUFFIX`` suffix.
    :return: A queue of files to download, and a queue of MD5 checksum to download.
        A queue is a dict containing as keys URLs of files to download and
        as values LocalFile instances containing metadata about the file that will be downloaded.
    """
    file_queue = {}
    checksum_queue = {}

    for url in urls:
        filename = Url.get_path_filename(url)
        filepath = Path(output_dir / filename)
        is_partially_downloaded = filename in partially_downloaded_files

        if filepath.suffix == ".md5":
            checksum_queue[url] = LocalFile(
                filename,
                FileType.CHECKSUM,
                filepath,
                is_partially_downloaded,
            )
        else:
            file_queue[url] = LocalFile(
                filename,
                FileType.FILE,
                filepath,
                is_partially_downloaded,
            )

    return file_queue, checksum_queue
