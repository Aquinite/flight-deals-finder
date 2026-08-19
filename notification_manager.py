import requests
import os
from dotenv import load_dotenv

load_dotenv()

class NotificationManager:
    """Handles telegram messaging for the flight finder script."""
    def __init__(self):
        self.chat_id = os.getenv("TG_CHAT_ID")
        self.tg_bot_token = os.getenv("TG_BOT_TOKEN")
        self.tg_url = f"https://api.telegram.org/bot{self.tg_bot_token}/sendMessage"
        self.tg_message = None
        self.tg_parameters = None

    def send_alert_message(self, price, departure_date, return_date, origin, destination, airline):
        """Sends an alert message to the user through Telegram regarding the cheapest flight found."""
        self.tg_message = (f"🚨Alert! Flight from {origin} to {destination} is now at an all time low at Php {price}!"
                           f"\n\nThis flight will be on {departure_date} to {return_date} under {airline}."
                           f"\n\nGo check the airline's website now!")

        self.tg_parameters = {"chat_id": self.chat_id, "text": self.tg_message}
        response = requests.get(url=self.tg_url, params=self.tg_parameters)
        response.raise_for_status()
        print(response.text)

    def no_flights_available_message(self, destination):
        """Sends the user a message indicate that there is no flight available within the timespan indicated."""
        self.tg_message = f"No flights available outbound to {destination} with your chosen dates! Keep waiting."
        self.tg_parameters = {"chat_id": self.chat_id, "text": self.tg_message}
        response = requests.get(url=self.tg_url, params=self.tg_parameters)
        response.raise_for_status()
        print(response.text)

    def no_lowest_price_message(self, destination):
        """Sends the user a message indicate that there is no flight available within the timespan indicated for their desired price."""
        self.tg_message = f"No flights available with desired price to {destination}! Keep waiting."
        self.tg_parameters = {"chat_id": self.chat_id, "text": self.tg_message}
        response = requests.get(url=self.tg_url, params=self.tg_parameters)
        response.raise_for_status()
        print(response.text)
