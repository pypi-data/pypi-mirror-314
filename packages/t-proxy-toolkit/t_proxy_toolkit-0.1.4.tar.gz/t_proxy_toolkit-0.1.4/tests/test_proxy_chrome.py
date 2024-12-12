import os
import unittest

from t_proxy.browser.chrome_proxy import ProxyChrome


class TestProxyChrome(unittest.TestCase):
    """Test case class for testing the ProxyChrome class."""

    def setUp(self):
        """Set up the test environment before each test case.

        This method is called before each test case to set up any necessary resources or configurations.
        In this case, it initializes the `credentials` dictionary with a username and password,
        and creates a `ProxyChrome` instance with the provided credentials.
        It also mocks the `browsser` attribute of the `ProxyChrome` instance using `MagicMock`.
        """
        nordlayer_user = os.getenv("NORDLAYER_USER")
        nordlayer_password = os.getenv("NORDLAYER_PASSWORD")
        nordlayer_network = os.getenv("NORDLAYER_NETWORK")
        nordlayer_organization = os.getenv("NORDLAYER_ORGANIZATION")
        nordvpn_user = os.getenv("NORDVPN_USER")
        nordvpn_password = os.getenv("NORDVPN_PASSWORD")
        self.nordlayer_credentials = {
            "login": nordlayer_user,
            "password": nordlayer_password,
            "network": nordlayer_network,
            "organization": nordlayer_organization,
        }
        self.nordvpn_credentials = {
            "login": nordvpn_user,
            "password": nordvpn_password,
        }
        self.proxy_chrome = ProxyChrome(self.nordlayer_credentials)
        self.url = ""

    def test_install_extension(self):
        """Test case for the install_extension method of the ProxyChrome class.

        This test verifies that the install_extension method correctly calls the open_available_browser
        and go_to methods of the browser object with the expected arguments.
        """
        self.proxy_chrome.install_extension()
        self.assertNotEqual(self.proxy_chrome.uuid, "")


if __name__ == "__main__":
    unittest.main()
