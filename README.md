# Flight Deals Finder

A Python script that checks flight prices from Manila (MNL) to a list of destinations stored in a Google Sheet, and sends a Telegram alert whenever it finds a price lower than the current recorded low.

## How it works

1. **Reads travel destinations from Google Sheets** via the [Sheety](https://sheety.co/) API — each row holds a destination airport code and the lowest price either seen so far by the API or manually set by the sheet owner.
2. **Searches flights with [SerpAPI's Google Flights endpoint](https://serpapi.com/google-flights-api)** across a set of dates (currently checks flights based on tomorrow's date and a month from tomorrow) for each destination. 
3. **Finds the cheapest flight per destination** across all dates checked. Flight price is based on a 1-week trip but can be changed inside the code. 
4. **Compares against the stored lowest price** in the sheet. If the new price is lower, it updates the sheet and sends a Telegram alert with the price, dates, and airline.
5. **Sends email alerts to signed-up users if new low is found** New feature: Create a Google form collecting emails of different users. Then, using the emails saved in the Google Form, it will send them the same alert sent on Telegram. Allows other users to receive flight alerts as well. 
6. **Sends a separate Telegram notification** if no flights are found at all for a destination across every date checked or if no flight matches the desired price set in the Google Sheet. 

## Other explanations
- Uses requests-cache as to not use up SerpAPI calls during testing as there is a 250 call limit for free tiers
- Uses sheety to quickly pull data from Google Sheets for usage in the 


## Future improvements
- Add return-date flexibility instead of a fixed one-week trip length in a user friendly way rather than it being hardcoded.
- Adding user-friendly way to change the set of dates used for checking flight availability.



## Setup

1. Clone the repo and install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Create a `.env` file (or set environment variables) with:
   ```
   SERP_API_KEY=your_serpapi_key
   SHEETY_ENDPOINT=your_sheety_endpoint
   SHEETY_USERNAME=your_sheety_username
   SHEETY_PASSWORD=your_sheety_password
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   TELEGRAM_CHAT_ID=your_telegram_chat_id
   MY_EMAIL=sender_email_for_email_alerts
   E_PASSWORD=app_password_generated_for_email_of_choice
   ```
3. Set up a Google Sheet with columns for destination IATA code and lowest recorded price, connected via Sheety. Sample sheet: https://docs.google.com/spreadsheets/d/1dR9peu1uvUyjUhffpoA37r3XI7bzgOq8aXRTN-qSZM0/edit?usp=sharing
4. Run the script:
   ```
   python main.py
   ```
