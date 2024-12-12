"""Config."""
from pathlib import Path


class CONFIG:
    """Configuration class for storing paths and settings."""

    class PATHS:
        """Paths for the module."""

        BASE = Path(__file__).parent
        CHROME_EXTENSION_PATH = BASE / "bin" / "latest.crx"
        FIREFOX_EXTENSION_PATH = BASE / "bin" / "latest.xpi"

    class URLS:
        """URLs for the module."""

        PROXY_SERVER = (
            'https://nordvpn.com/wp-admin/admin-ajax.php?action=servers_recommendations&filters={"country_id":228}'
        )
        FIREFOX_EXTENSION_URL = "https://downloads.nordlayer.com/ext/latest.xpi"
