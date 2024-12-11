import hashlib
from pathlib import Path

from tqdm import tqdm

from cnrgh_dl.logger import Logger
from cnrgh_dl.models import (
    DownloadResults,
    DownloadStatus,
    LocalFiles,
)

logger = Logger.get_instance()
"""Module logger instance."""


class Integrity:
    """Groups methods used to check the integrity of downloaded files."""

    @staticmethod
    def _parse_checksum_file(filepath: Path) -> tuple[str, str]:
        """Parses an MD5 checksum file.

        The file content should be formatted as follows:

        ``<MD5 checksum>  <filename>``

        Example:
        --------
        ``702edca0b2181c15d457eacac39de39b  test.txt``

        :param filepath: The path of the MD5 file to parse.
        :raises ValueError: If the file is empty or incorrectly formatted.
        :return: A tuple containing in the first position the hash,
            and in the second position the filename.
        """
        with Path.open(filepath) as f:
            first_line = f.readline()
            if not first_line:
                msg = "Empty file."
                raise ValueError(msg)
            try:
                file_hash, file_name = first_line.split()
            except ValueError as err:
                msg = "Hash or filename is missing."
                raise ValueError(msg) from err
            return file_hash, file_name

    @staticmethod
    def _compute_checksum(filepath: Path) -> str:
        """Computes the MD5 checksum of a file.

        :param filepath: The path of the file to compute the checksum for.
        :return: The computed checksum.
        """
        chunk_num_blocks = 128
        h = hashlib.md5()
        file_size = filepath.stat().st_size

        with tqdm(
            total=file_size,
            unit="B",
            unit_scale=True,
            miniters=1,
            desc=f"{filepath.name} MD5 compute",
            leave=False,
        ) as t:
            with Path.open(filepath, "rb") as f:
                while chunk := f.read(chunk_num_blocks * h.block_size):
                    h.update(chunk)
                    t.update(len(chunk))

            t.update(abs(file_size - t.n))
            t.close()

        return h.hexdigest()

    @staticmethod
    def check(
        file_queue: LocalFiles,
        checksum_queue: LocalFiles,
        dl_results: DownloadResults,
    ) -> dict[str, str]:
        """Check the integrity of downloaded files against their downloaded checksums.

        :param file_queue: Queue of files to download.
        :param checksum_queue: Queue of checksums to download.
        :param dl_results: Dict containing download results.
        :returns: A dict containing as keys file URLs and as values the message returned by the integrity check.
            This dict is only returned for testing purposes.
        """
        res = {}

        for url, local_file in file_queue.items():
            checksum_url = f"{url}.md5"
            local_file_dl_results = dl_results[url]

            # If the file download encountered an error, we skip the check.
            if local_file_dl_results.status is not DownloadStatus.SUCCESS:
                msg = f"Skipping {local_file.filename}: the file was not downloaded."
                res[url] = msg
                logger.warning(msg)
                continue

            # If no checksum corresponding to the file was downloaded, we skip the check.
            if checksum_url not in checksum_queue:
                msg = f"Skipping {local_file.filename}: no corresponding checksum was downloaded."
                res[url] = msg
                logger.warning(msg)
                continue

            checksum_dl_results = dl_results[checksum_url]

            # If the checksum download encountered an error, we skip the check.
            if checksum_dl_results.status is not DownloadStatus.SUCCESS:
                msg = f"Skipping {local_file.filename}: its corresponding checksum was not downloaded."
                res[url] = msg
                logger.warning(msg)
                continue

            # Here, we are sure that the file was successfully downloaded along its checksum.
            try:
                checksum_path = checksum_queue[checksum_url].path

                (file_checksum, file_name) = Integrity._parse_checksum_file(
                    checksum_path,
                )
                is_valid = file_checksum == Integrity._compute_checksum(
                    local_file.path,
                )

                if is_valid:
                    msg = f"Integrity check success: the file {local_file.filename} matches its checksum."
                    res[url] = msg
                    logger.info(msg)
                else:
                    msg = f"Integrity check error: the file {local_file.filename} does not match its checksum."
                    res[url] = msg
                    logger.error(msg)

            except ValueError:
                msg = (
                    f"Integrity check error: can't check the file {local_file.filename} as "
                    f"its checksum {checksum_dl_results.filename} is incorrectly formatted."
                )
                res[url] = msg
                logger.error(msg)

        return res
