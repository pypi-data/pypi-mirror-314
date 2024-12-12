from typing import Union

from selenium.webdriver.chrome.options import Options

from t_proxy.browser.chrome_proxy import ProxyChrome
from t_proxy.browser.firefox_proxy import ProxyFirefox
from t_proxy.requests.requests_proxy import ProxyRequests


class BrowserProxy:
    """Class for creating browser with proxy extension installed and connected to the gateway."""

    def chrome(
        self,
        user: str,
        password: str,
        network: str,
        organization: str = "thoughtful",
        options: Union[Options, None] = None,
    ):
        """Create Chrome browser with proxy extension installed and connected to the gateway."""
        proxy_chrome = ProxyChrome(user, password, network, organization, options)
        proxy_chrome.start()
        return proxy_chrome.browser

    def firefox(
        self,
        user: str,
        password: str,
        network: str,
        organization: str = "thoughtful",
        options: Union[dict, None] = None,
    ):
        """Create Firefox browser with proxy extension installed and connected to the gateway."""
        proxy_firefox = ProxyFirefox(user, password, network, organization, options)
        proxy_firefox.start()
        return proxy_firefox.browser


class RequestsProxy:
    """Class for creating a session with proxy connected to the gateway."""

    def session(self, credentials: dict):
        """Create a session with proxy connected to the gateway."""
        proxy_requests = ProxyRequests(credentials)
        return proxy_requests.session
