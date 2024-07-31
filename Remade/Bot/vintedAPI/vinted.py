from .Items import Items
from .requester import Requester

class Vinted:
    def __init__(self, country_code, proxy=None):
        self.requester = Requester(country_code)
        
        if proxy is not None: # limit bypass
            self.requester.session.proxies.update(proxy)

        self.items = Items(country_code)