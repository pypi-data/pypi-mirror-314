import json
import time

import requests

from t_proxy.browser.t_proxy_core import BrowserProxyCore
from t_proxy.config import CONFIG
from t_proxy.exceptions import (
    EnablePrivateBrowsingException,
    ExtensionDownloadException,
    ExtensionEmptyUUIDException,
    ExtensionInstallException,
)
from t_proxy.utils.logger import logger


class ProxyFirefox(BrowserProxyCore):
    """Class for Firefox."""

    def __init__(self, user: str, password: str, network: str, organization: str, options: dict):
        """Initializes a FirefoxProxy object.

        Args:
            credentials (dict): A dictionary containing the credentials for the proxy.

        Returns:
            None
        """
        super().__init__(user, password, network, organization)
        self.options = options

    def start(self):
        """Starts the Firefox proxy.

        This method performs the necessary steps to start the Firefox proxy, including downloading the extension,
        opening the browser, installing the extension, getting the extension UUID, logging in to the extension,
        and testing the connection.
        """
        # self.__download_extension()
        self.open_browser()
        self.install_extension()
        self.obtain_extension_uuid()
        url = self.firefox_extension_url.format(self.uuid)
        self.login_on_extension(url)
        self.test_connection()

    def open_browser(self):
        """Open Firefox browser."""
        try:
            logger.debug("Opening Firefox browser...")
            self.browser.open_available_browser(
                user_agent=self.user_agent.firefox, preferences=self.options, browser_selection="firefox"
            )
        except Exception as ex:
            logger.exception(ex)
            raise Exception(f"Module failed to open Firefox browser: {ex}")

    def __download_extension(self):
        """Download NordLayer extension from the URL in Bitwarden.

        If failed to download, raises exception.
        """
        logger.debug("Downloading NordLayer extension...")
        try:
            response = requests.get(CONFIG.URLS.FIREFOX_EXTENSION_URL)
            with open(CONFIG.PATHS.FIREFOX_EXTENSION_PATH, mode="wb") as f:
                f.write(response.content)
            logger.debug("NordLayer extension downloaded successfully")
        except Exception as ex:
            logger.exception(ex)
            raise ExtensionDownloadException("Module failed to download NordLayer extension")

    def install_extension(self):
        """Install NordLayer extension to firefox browser.

        time.sleep(5) is required, cause without it, extension is being stuck on loading spinner
        and module is not able to login and connect to the gateway.
        If failed to install, raises exception.
        """
        logger.debug("Installing NordLayer extension...")
        try:
            self.id = self.browser.driver.install_addon(CONFIG.PATHS.FIREFOX_EXTENSION_PATH)
            time.sleep(5)
            self.allow_private_browsing_ui()
        except Exception as ex:
            logger.exception(ex)
            raise ExtensionInstallException("Module failed to install NordLayer extension")

    def obtain_extension_uuid(self):
        """Obtain installed extension uuid for future use.

        If failed to get uuid, raises exception.
        """
        logger.debug("Getting extension uuid...")
        profile_path = self.browser.driver.capabilities["moz:profile"]
        with open("{}/prefs.js".format(profile_path), "r") as file_prefs:
            lines = file_prefs.readlines()
            for line in lines:
                if "extensions.webextensions.uuids" in line:
                    extensions = json.loads(line[45:-4].replace("\\", ""))
                    if self.id in extensions:
                        self.uuid = extensions[self.id]
                        break
        if self.uuid == "":
            raise ExtensionEmptyUUIDException("Module failed to get installed extension uuid")
        logger.debug(f"Extension uuid is: {self.uuid}")

    def allow_private_browsing_ui(self):
        """Enable private browsing for NordLayer extension.

        This is required to be able to use extension as a VPN/Proxy layer.
        If failed to enable private browsing, raises exception.
        """
        logger.debug("Enabling extension private browsing...")
        self.browser.go_to("about:addons")
        self.browser.wait_until_element_is_visible('//button[@title="Extensions"]')
        self.browser.click_button_when_visible('//button[@title="Extensions"]')
        clicked = False
        for _ in range(0, 10):
            try:
                self.browser.execute_javascript(f"document.querySelector('[addon-id=\"{self.id}\"]').click()")
                self.browser.execute_javascript('document.getElementsByName("private-browsing")[0].click()')
                clicked = True
                break
            except Exception as ex:
                logger.exception(ex)
        self.browser.wait_until_element_is_visible('//button[@title="Extensions"]')
        self.browser.click_button_when_visible('//button[@title="Extensions"]')
        if not clicked:
            raise EnablePrivateBrowsingException("Failed to enable private browsing")
