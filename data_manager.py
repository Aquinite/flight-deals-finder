import os
from dotenv import load_dotenv
from requests_cache_manager import session
load_dotenv()

class SheetDataManager:
    """This class is responsible for talking to the Google Sheet."""
    def __init__(self):
        self.sheet_flight_data = {}
        sheety_url = os.getenv("SHEETY_BASE_URL")
        self.get_put_sheety_url = f"{sheety_url}/flightDeals/prices"
        # self.put_sheety_url = f"{sheety_url}/flightDeals/prices/[Object ID (apparently just the row number)]"
        self.sheety_headers = {"Authorization": f"Bearer {os.getenv('SHEETY_TOKEN')}"}

    def get_sheet_data(self):
        """Pulls the sheet data currently available from Sheety API."""
        sheet_data = session.get(url=self.get_put_sheety_url, headers=self.sheety_headers)
        sheet_data.raise_for_status()
        self.sheet_flight_data = sheet_data.json()
        return self.sheet_flight_data

    def update_lowest_price(self,row_number,new_price):
        """Updates the lowest price for the city indicated in your Google Sheet."""
        put_sheety_url = f"{self.get_put_sheety_url}/{row_number}"
        params = {
            "price": {
            "lowestPrice": new_price
            }
        }
        request = session.put(url=put_sheety_url, json=params, headers=self.sheety_headers)
        request.raise_for_status()


    # structured in the ff way:
    # 1. Dictionary containing the prices key
    # 2. Prices key returns a list with each item in list being a dictionary that contains the header, then value of each row.
    #     {'prices': [{'city': 'Bali', 'iataCode': 'DPS', 'lowestPrice': 22000, 'id': 2},
    #     {'city': 'Cebu', 'iataCode': 'CEB', 'lowestPrice': 4000, 'id': 3},
    #     {'city': 'Tokyo', 'iataCode': 'HND', 'lowestPrice': 22000, 'id': 4}]}
