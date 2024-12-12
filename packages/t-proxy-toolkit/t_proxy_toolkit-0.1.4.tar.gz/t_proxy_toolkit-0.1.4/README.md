# t-proxy-toolkit #
 This is a wrapper around rpaframework selenium driver to enable a proxy using NordLayer. You can use this too to start a request session using NordVPN

# How do I get set up? #

* To install it just run

      `pip install t-proxy-toolkit`

# How to integrate this in my code #

## For browser usage ##

Instead of creating a new selenium object from rpaframework, call this library with the method `chrome` or `firefox` and optional, the init preferences or options to the browser in a dict.

By default, the browser will assign a custom UserAgent using the fake-useragent package and this settings and the correct ua if the browser open is chrome or firefox:

```
user_agent = UserAgent(os="windows", min_percentage=1.3)

# For chrome
user_agent.chrome

# For firefox
user_agent.firefox
```

:bangbang: :warning: It's a known issue that you can't use headless when you're trying to install an extension :warning: :bangbang:


```python
from t_proxy import BrowserProxy
from RPA.Browser.Selenium import Selenium

browser_proxy = BrowserProxy()

# get this from bitwarden
user = "" # user
password = "" # pwd
organization = "thoughtful" # should be thoughtful always
network = "" # name of the network to use


# call the browser you want to use, set the variable to Selenium class to enable the autocomplete

firefox: Selenium = browser_proxy.firefox(user, password, network, organization)
chrome: Selenium = browser_proxy.chrome(user, password, network, organization)
```

## Setup preferences or options ##
For firefox you can send parameters to the browser object with a dictionary. The full list of preferences in the following links:

* [firefox.js](https://searchfox.org/mozilla-release/source/browser/app/profile/firefox.js)
* [all.js](https://searchfox.org/mozilla-release/source/modules/libpref/init/all.js)
* [StaticPrefList.yaml](https://searchfox.org/mozilla-release/source/modules/libpref/init/StaticPrefList.yaml)

```python
prefs: dict = {
            "download.default_directory": "some/path/to/output",
      }

firefox: Selenium = browser_proxy.firefox(user, password, network, organization, prefs)
```

For chrome you can send parameters to the browser object with the options object from selenium chrome. The full list of preferences in the following links:

* [Chronium command line switches](https://peter.sh/experiments/chromium-command-line-switches/)
* [chrome_switches.cc](https://chromium.googlesource.com/chromium/src/+/master/chrome/common/chrome_switches.cc)
* [For search switches](https://source.chromium.org/search?q=file:switches.cc&ss=chromium%2Fchromium%2Fsrc)

```python
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--no-sandbox")

chrome: Selenium = browser_proxy.chrome(user, password, network, organization, options)
```



## For requests usage ##
This will use the Oxylabs servers available and will start a requests session with the https proxy enabled.

If port is 8000, it will return a different IP on every request.

If port is 8001 to 8010, it will use a fixed IP all the time.

IPs can be changed anytime from Oxylabs dashboard.

```python
from t_proxy import RequestsProxy
from requests import Session

# get this from bitwarden
creds = {
      "login": "", # user
      "password": "", # pwd
      "port": ""
}
requests_proxy = RequestsProxy()
session: Session = session.session(creds)

# make your requests calls.
response = session.get("https://api.ipify.org?format=json")
print(response.json())

```


## Current bots using this tool ##


Bot Code | Firefox | Chrome | Requests |
--- | --- | --- | --- |
DMA2 | :white_check_mark: | :x: | :x: |
SD2 | :x: | :x: | :white_check_mark: |