import requests
import os
from dotenv import load_dotenv
import smtplib

load_dotenv()

class NotificationManager:
    """Handles telegram messaging for the flight finder script."""
    def __init__(self):
        self.chat_id = os.getenv("TG_CHAT_ID")
        self.tg_bot_token = os.getenv("TG_BOT_TOKEN")
        self.my_email = os.getenv("MY_EMAIL")
        self.my_password = os.getenv("E_PASSWORD")
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

    def send_email_users(self,price, departure_date, return_date, origin, destination, airline, users):
        """Sends an email message to users signed up on the service."""
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            users = users
            message = (f"Subject:Best flight for you!\n\n"
                       f"🚨Alert! Flight from {origin} to {destination} is now at an all time low at Php {price}!"
                       f"\n\nThis flight will be on {departure_date} to {return_date} under {airline}."
                       f"\n\nGo check the airline's website now!")
            connection.login(user=self.my_email, password=self.my_password)
            connection.sendmail(from_addr=self.my_email,to_addrs=users,msg= message.encode("utf-8"))


    def no_flights_available_message(self, destination):
        """Sends the user a Telegram message indicate that there is no flight available within the timespan indicated."""
        self.tg_message = f"No flights available outbound to {destination} with your chosen dates! Keep waiting."
        self.tg_parameters = {"chat_id": self.chat_id, "text": self.tg_message}
        response = requests.get(url=self.tg_url, params=self.tg_parameters)
        response.raise_for_status()
        if response.status_code != 200:
            status_code = response.status_code
            print(f"Message not sent. Status Code: {status_code}")

    def no_lowest_price_message(self, destination):
        """Sends the user a Telegram message to indicate that there is no flight available within the timespan indicated for their desired price."""
        self.tg_message = f"No flights available with desired price to {destination}! Keep waiting."
        self.tg_parameters = {"chat_id": self.chat_id, "text": self.tg_message}
        response = requests.get(url=self.tg_url, params=self.tg_parameters)
        response.raise_for_status()
        if response.status_code != 200:
            status_code = response.status_code
            print(f"Message not sent. Status Code: {status_code}")