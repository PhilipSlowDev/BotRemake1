class Urls:
    def __init__(self, country_code):
        self.VINTED_API_URL = f"https://www.vinted.{country_code}/api/v2"
        self.VINTED_PRODUCTS_ENDPOINT = "catalog/items"