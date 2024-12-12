class ExtensionInstallException(Exception):
    """Exception raised when module failed to install NordLayer extension."""

    ...


class ExtensionEmptyUUIDException(Exception):
    """Exception raised when failed to get uuid of installed extension."""

    ...


class EnablePrivateBrowsingException(Exception):
    """Exception raised when failed to enable private browsing in Firefox."""

    ...


class IPAddressValidationException(Exception):
    """Exception raised when proxy connection is not working."""

    ...


class ExtensionNotConnectedException(Exception):
    """Exception raised when extension was not able to connect to the proxy."""

    ...


class ExtensionDownloadException(Exception):
    """Exception raised when module failed to download NordLayer extension."""

    ...
