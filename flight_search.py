import os
from dotenv import load_dotenv
from requests_cache_manager import session


load_dotenv()

class FlightSearch:
    """This class is responsible for talking to the Flight Search API."""
    def __init__(self, from_place, to_place, departure_date, return_date):
        self.serp_endpoint = "https://serpapi.com/search?engine=google_flights"
        self.api_key = os.getenv("SERP_API_KEY")
        self.serp_parameters = {"engine": "google_flights",
                                "departure_id": from_place,
                                "arrival_id": to_place,
                                "outbound_date": departure_date,
                                "return_date": return_date,
                                "type": "1",
                                "adults": "1",
                                "currency": "PHP",
                                "api_key": self.api_key}
        self.flight_is_direct = True
        self.cheapest_flight_data = None

    def search_flights(self):
        """Searches for available flights based on parameters passed from init then returns a list of the flights available for that date."""
        flight_data = session.get(url=self.serp_endpoint, params=self.serp_parameters)
        flight_data.raise_for_status()
        flight_data_json = flight_data.json()
        best_flights_data = flight_data_json.get("best_flights",[])
        #by adding a default value of [], we don't let the thing crash if there's no best flights data.
        other_flights_data = flight_data_json.get("other_flights",[])
        return best_flights_data + other_flights_data
        #returns a combined list with all the data from the API, make sure to only get best flights and other flights data

    def check_cheapest_flight(self):
        """Returns the cheapest flight from the search flights method."""
        flight_data = self.search_flights()
        if not flight_data:
            return flight_data
        else:
            new_flight_data = [flight for flight in flight_data if "price" in flight]
                #filters every flight in the returned flight data and returns a new list with flights that contain a price key
                #prevents program from giving us flights with a missing price key or else checking for the min will crash the program
            cheapest_flight = min(new_flight_data, key=lambda f: f["price"])
            return cheapest_flight
            # using the combined flight data, pull the flight with the cheapest price in the list,
            # then return it and pass it on to cheapest_flight_data so that we can compare that data with the cheapest price in sheety.








