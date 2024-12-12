import requests
from retry import retry

from t_proxy.exceptions import IPAddressValidationException
from t_proxy.utils import logger


class ProxyRequests:
    """Class for creating a session with proxy extension installed and connected to the gateway."""

    def __init__(self, credentials: dict):
        """Initializes a new instance of the RequestsProxy class.

        Args:
            credentials (dict): A dictionary containing the credentials for the proxy server.

        Attributes:
            credentials (dict): The credentials for the proxy server.
            server (str): The proxy server URL.
            session (requests.Session): The session object for making HTTP requests.
            initial_ip (str): The initial IP address before connecting to the proxy server.
        """
        self.credentials = credentials
        self.server = "isp.oxylabs.io"
        self.session = requests.Session()
        self.initial_ip = self.__get_current_ip()
        self._set_session_proxy()
        self.test_connection()

    def _set_session_proxy(self):
        """Create a session with the specified VPN credentials and server.

        Returns:
            requests.Session: A session object with the specified VPN settings.
        """
        vpn_login = self.credentials["login"]
        vpn_password = self.credentials["password"]
        vpn_server = self.server
        vpn_port = self.credentials["port"]
        proxies = {
            "https": f"https://{vpn_login}:{vpn_password}@{vpn_server}:{vpn_port}",
        }
        self.session.proxies = proxies
        return self.session

    @retry(tries=3, delay=5)
    def __get_current_ip(self):
        """Retrieves the current IP address by making a request to the ipify API.

        Returns:
            str: The current IP address.

        Raises:
            Exception: If the request to the ipify API fails.
        """
        response = self.session.get("https://api.ipify.org?format=json")
        if response.status_code == 200:
            ip = response.json()["ip"]
            logger.info(f"Current IP: {ip}")
            return ip

    def test_connection(self):
        """Test if proxy connection is working by checking IP address.

        If IP address is the same as initial, raises exception.
        """
        logger.debug("Testing proxy connection...")
        ip = self.__get_current_ip()
        if ip != self.initial_ip:
            logger.debug(f"Proxy connection is working. IP: {ip}")
        else:
            logger.exception(f"Proxy connection is not working. IP: {ip}")
            raise IPAddressValidationException("Proxy connection is not working.")
