import requests
from requests.exceptions import HTTPError

MAX_RETRIES = 3
class Requester:

    def __init__(self, country_code):
        self.session = requests.Session()
        self.update_headers_and_url(country_code)

    def update_headers_and_url(self, country_code):
        self.session.headers.update({
            "User-Agent": "PostmanRuntime/7.28.4",
            "Host": f"www.vinted.{country_code}",
        })
        self.VINTED_AUTH_URL = f"https://www.vinted.{country_code}/auth/token_refresh"

    def get(self, url, params=None):
        tried = 0
        while tried < MAX_RETRIES:
            tried += 1
            with self.session.get(url, params=params) as response:
                if response.status_code == 401 and tried < MAX_RETRIES:
                    print(f"Cookies invalid retrying {tried}/{MAX_RETRIES}")
                    self.setCookies()
                elif response.status_code == 200 or tried == MAX_RETRIES:
                    return response
        return HTTPError

    def post(self, url, params=None):
        response = self.session.post(url, params)
        response.raise_for_status()
        return response

    def setCookies(self):
        self.session.cookies.clear_session_cookies()
        try:
            self.post(self.VINTED_AUTH_URL)
            print("Cookies set!")
        except Exception as e:
            print(f"There was an error fetching cookies for vinted\n Error : {e}")

requester = None

def get_requester(country_code):
    global requester
    if requester is None:
        requester = Requester(country_code)
    return requester