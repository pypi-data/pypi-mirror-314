import json

from fake_useragent import UserAgent
from retry import retry
from RPA.Browser.Selenium import Selenium
from SeleniumLibrary.errors import NoOpenBrowser

from t_proxy.exceptions import ExtensionNotConnectedException, IPAddressValidationException
from t_proxy.utils.logger import logger


class BrowserProxyCore:
    """Core class for browser proxy."""

    def __init__(self, user: str, password: str, network: str, organization: str):
        """Initializes a new instance of the TProxyCore class.

        Args:
            credentials (dict): A dictionary containing the credentials for authentication.

        Attributes:
            id (str): The ID of the TProxyCore instance.
            uuid (str): The UUID of the TProxyCore instance.
            creds (dict): The credentials for authentication.
            browser (Selenium): The Selenium browser instance.
            initial_ip (str): The initial IP address obtained from __get_current_ip() method.
        """
        self.id = ""
        self.uuid = ""
        self.user = user
        self.password = password
        self.network = network
        self.organization = organization
        self.browser = Selenium()
        self.user_agent = UserAgent(os="windows", min_percentage=1.3)
        self.initial_ip = self.__get_current_ip()
        self._chrome_extension_url = "chrome-extension://{}/popup.html"
        self._firefox_extension_url = "moz-extension://{}/popup.html"

    def is_browser_open(self) -> bool:
        """Checks if the browser is open.

        Returns:
            bool: True if the browser is open, False otherwise.
        """
        try:
            return self.browser.driver is not None
        except NoOpenBrowser:
            return False

    def __get_current_ip(self):
        """Get current IP address using NordVPN page and ifconfig.me as a backup in case of failure."""
        logger.debug("Getting current IP...")

        driver_is_alive = self.is_browser_open()
        close_browser = False

        if not driver_is_alive:
            self.browser.open_available_browser()
            close_browser = True

        try:
            self.browser.go_to("http://httpbin.org/ip")
            self.browser.wait_until_element_is_visible("//pre")
            ip_literal = self.browser.get_text("//pre")
            ip_json = json.loads(ip_literal)
            ip = ip_json["origin"]
        except Exception as ex:
            logger.exception(ex)
            logger.warning("Failed to get IP from NordVPN page. Using ifconfig.me as a backup.")
            self.browser.go_to("https://ifconfig.me/")
            self.browser.wait_until_element_is_visible("//td[@id='ip_address_cell']")
            ip = self.browser.get_text("//td[@id='ip_address_cell']")
        if close_browser:
            self.browser.close_browser()

        return ip

    @property
    def chrome_extension_url(self):
        """Chrome_Extension_Url property."""
        return self._chrome_extension_url

    @property
    def firefox_extension_url(self):
        """Firefox_Extension_Url property."""
        return self._firefox_extension_url

    @retry(ExtensionNotConnectedException, tries=3, delay=5)
    def login_on_extension(self, url):
        """Login to NordLayer extension using credentials from Bitwarden.

        If extension was not able to connect to the gateway, raises exception.
        """
        logger.debug("Logging in to NordLayer extension...")
        next_button_xpath = '//button[contains(@class, "rounded")]'
        agree_button_xpath = '//button[contains(text(), "Agree and continue")]'
        organization_xpath = '//input[@id="organizationId"]'
        email_xpath = "//input[@id='email']"
        password_xpath = "//input[@id='password']"
        proxy_xpath = f"//span[contains(text(), '{self.network}')]"
        connected_xpath = "//label[contains(@class, 'text-green-bright') and contains(text(), 'Connected')]"
        not_connected_xpath = "//label[contains(@class, 'text-red') and contains(text(), 'Not connected')]"

        self._click_next_button(next_button_xpath, url)
        self.browser.click_element_when_visible(next_button_xpath)
        self.browser.wait_until_element_is_visible(organization_xpath)
        self.browser.input_text(organization_xpath, self.organization)
        self.browser.wait_until_element_is_visible(next_button_xpath)
        self.browser.click_element_when_visible(next_button_xpath)
        self.browser.wait_until_element_is_visible(email_xpath)
        self.browser.input_text(email_xpath, self.user)
        self.browser.wait_until_element_is_visible(password_xpath)
        self.browser.input_text(password_xpath, self.password)
        self.browser.wait_until_element_is_visible(next_button_xpath)
        self.browser.click_element_when_visible(next_button_xpath)
        self.browser.wait_until_element_is_visible(agree_button_xpath)
        self.browser.click_element_when_visible(agree_button_xpath)
        self.browser.wait_until_element_is_visible(proxy_xpath, timeout=10)
        self.browser.click_element_when_visible(proxy_xpath)
        try:
            self.browser.wait_until_element_is_visible(connected_xpath, timeout=120)
        except Exception as ex:
            if self.browser.does_page_contain_element(not_connected_xpath):
                logger.exception("Extension was not able to connect to the proxy.")
                raise ExtensionNotConnectedException("Extension was not able to connect to the proxy")
            else:
                logger.exception(ex)
                raise ex

    @retry(AssertionError, tries=5, delay=1)
    def _click_next_button(self, next_button_xpath: str, url: str):
        # Retry loop to wait for the next button to appear
        self.browser.go_to(url)
        self.browser.wait_until_element_is_visible(next_button_xpath, timeout=10)

    def test_connection(self):
        """Test the proxy connection by comparing the current IP address with the initial IP address.

        Returns:
            bool: True if the proxy connection is working, False otherwise.

        Raises:
            IPAddressValidationException: If the proxy connection is not working.
        """
        logger.debug("Testing proxy connection...")
        ip = self.__get_current_ip()
        if ip != self.initial_ip:
            logger.debug(f"Proxy connection is working. IP: {ip}")
        else:
            logger.exception(f"Proxy connection is not working. IP: {ip}")
            raise IPAddressValidationException("Proxy connection is not working.")
        return True
