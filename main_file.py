import datetime
from dateutil.relativedelta import relativedelta
from data_manager import SheetDataManager
from flight_search import FlightSearch
from cheapest_flight_data import CheapestFlightData
from notification_manager import NotificationManager

#Our Classes
data_manager = SheetDataManager()
notification_manager = NotificationManager()
sheet_data = data_manager.get_sheet_data()  # contains the sheet data needed for comparison

#Variables needed
ORIGIN_AIRPORT = "MNL" #NAIA
DATE_TOM = datetime.date.today() +datetime.timedelta(days=1)
DATES_TO_CHECK = [DATE_TOM + relativedelta(months=i) for i in range(2)] #checks dates within the next month (tom + a month from tom), can be customized

for city in sheet_data.get("prices"): #for each row in the sheet_data
    destination = city.get("iataCode")  #pull the iataCode
    flights_found = []
    for date in DATES_TO_CHECK:
        departure_date = date
        return_date = date + relativedelta(weeks=1)
        flight_searcher = FlightSearch(from_place=ORIGIN_AIRPORT,
                                       to_place= destination,
                                       departure_date=str(departure_date),
                                       return_date= str(return_date),)
        cheapest_flight = flight_searcher.check_cheapest_flight()
        if cheapest_flight:
            cheapest_flight_data = CheapestFlightData(cheapest_flight_data=cheapest_flight,
                                                      flight_return_date=str(return_date))
            flights_found.append(cheapest_flight_data)

    if not flights_found:
        notification_manager.no_flights_available_message(destination=destination)

    else:
        cheapest_flight_found = min(flights_found, key=lambda f: f.price)
        cheapest_flight_found_price = cheapest_flight_found.price
        if city.get("lowestPrice") > cheapest_flight_found_price:
            data_manager.update_lowest_price(row_number=city.get("id"), new_price=cheapest_flight_found_price)
            notification_manager.send_alert_message(price=cheapest_flight_found_price,
                                                    departure_date=cheapest_flight_found.departure_date,
                                                    return_date=cheapest_flight_found.return_date,
                                                    airline=cheapest_flight_found.airline,
                                                    origin=ORIGIN_AIRPORT,
                                                    destination=destination,
                                                    )
        else:
            notification_manager.no_lowest_price_message(destination=destination)
            # if price isn't lower than our set lowest price, sends message that there are no flights available with desired price.