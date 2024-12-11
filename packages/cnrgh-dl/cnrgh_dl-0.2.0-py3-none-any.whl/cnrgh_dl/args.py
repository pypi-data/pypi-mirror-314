import argparse
from importlib.metadata import version
from pathlib import Path


def get_args() -> argparse.Namespace:
    """Parses the arguments needed by the program.

    :return: A Namespace object holding parsed arguments and their values.
    """
    parser = argparse.ArgumentParser(
        prog="cnrgh-dl",
        description="Python client for downloading CNRGH project data.",
    )
    parser.add_argument(
        "outdir",
        type=Path,
        help="Output directory where downloaded files are stored.",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {version(__package__)}",
    )
    parser.add_argument(
        "-i",
        "--input-file",
        type=Path,
        help="Path to a file containing a list of URLs to download (one per line). "
        "Without this argument, cnrgh-dl will run in 'interactive' mode and "
        "ask for a list of files to download via the standard input.",
    )
    parser.add_argument(
        "--no-integrity-check",
        action="store_true",
        help="By default, cnrgh-dl will check the integrity of each downloaded file if "
        "its checksum file is present in the download queue. Using this option will disable this behavior: "
        "the integrity of downloaded files will not be checked.",
    )
    parser.add_argument(
        "--no-additional-checksums",
        action="store_true",
        help="By default, cnrgh-dl will try to download additional checksums for "
        "files in the download queue. "
        "If a file is listed in the queue without its checksum, "
        "cnrgh-dl will automatically download its checksum "
        "if it exists on the datawebnode server. "
        "If the checksum of a file is not available on the server, "
        "the verification will fail with the following message: "
        "'No corresponding MD5 file found.'. Using this option will disable this behavior: "
        "only the files explicitly listed in the download queue will be downloaded.",
    )
    parser.add_argument(
        "-f",
        "--force-download",
        action="store_true",
        help="By default, cnrgh-dl will skip the download of a file "
        "if it is already present in the output directory. "
        "If a file is partially downloaded (e.i. its filename is prefixed by '.part'), its download will continue. "
        "Using this option will re-download all files already present in the output directory, "
        "whether their download is complete or partial.",
    )
    parser.add_argument(
        "-j",
        "--json-report",
        action="store_true",
        help="Write a JSON report about downloaded files in the output directory.",
    )
    return parser.parse_args()
