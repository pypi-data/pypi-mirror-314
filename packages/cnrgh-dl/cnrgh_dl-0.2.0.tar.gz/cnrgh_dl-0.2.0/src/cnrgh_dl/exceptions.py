from typing_extensions import Self


class PrematureDownloadTerminationError(Exception):
    """Exception raised when a download finishes prematurely."""

    def __init__(self: Self) -> None:
        """Initialize a PrematureDownloadTerminationError Exception."""
        super().__init__(
            "Download prematurely terminated. "
            "The server may not have sent all the data or there was a network issue.",
        )


class MissingScopesError(Exception):
    """Exception raised when the server did not grant all the requested scopes."""

    def __init__(self: Self, missing_scopes: set[str]) -> None:
        """Initialize a MissingScopesError Exception."""
        self.missing_scopes = missing_scopes
        super().__init__(
            f"Some scopes were not granted by the authorization server "
            f"and are missing: {','.join(missing_scopes)}."
        )
