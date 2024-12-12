import json
import time

from selenium.webdriver.chrome.options import Options

from t_proxy.browser.t_proxy_core import BrowserProxyCore
from t_proxy.config import CONFIG
from t_proxy.exceptions import ExtensionEmptyUUIDException, ExtensionInstallException
from t_proxy.utils.logger import logger


class ProxyChrome(BrowserProxyCore):
    """Class for Chrome browser proxy."""

    def __init__(self, user: str, password: str, network: str, organization: str, options: Options):
        """Initializes a ProxyChrome object.

        Args:
            credentials (dict): A dictionary containing the credentials for the proxy.

        Returns:
            None
        """
        super().__init__(user, password, network, organization)
        self.options = options if options else Options()

    def start(self):
        """Starts the Chrome proxy.

        This method installs the extension, gets the extension URL,
        logs in to the extension, and tests the connection.
        """
        self.install_extension()
        url = self.chrome_extension_url.format(self.uuid)
        self.login_on_extension(url)
        self.test_connection()

    def install_extension(self):
        """Install NordLayer extension to chrome browser.

        time.sleep(5) is required, cause without it, extension is being stuck on loading spinner
        and module is not able to login and connect to the gateway.
        If failed to install, raises exception.
        """
        logger.debug("Installing NordLayer extension...")
        try:
            self.options.add_extension(CONFIG.PATHS.CHROME_EXTENSION_PATH)
            self.browser.open_available_browser(
                user_agent=self.user_agent.chrome, browser_selection="chrome", options=self.options
            )
            self.obtain_extension_uuid()
            time.sleep(5)

        except Exception as ex:
            logger.exception(ex)
            raise ExtensionInstallException("Module failed to install NordLayer extension")

    def obtain_extension_uuid(self):
        """Get installed extension uuid for future use.

        If failed to get uuid, raises exception.
        """
        logger.debug("Getting extension uuid...")
        self.browser.go_to("chrome://extensions-internals/")
        internals_json = self.browser.get_webelement("//pre").text
        internals = json.loads(internals_json)
        for extension in internals:
            if "NordLayer" in extension.get("name", ""):
                self.uuid = extension["id"]
                break
        else:
            raise ExtensionEmptyUUIDException("Module failed to get installed extension uuid")
        logger.debug(f"Extension uuid is: {self.uuid}")
