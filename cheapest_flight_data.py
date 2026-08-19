class CheapestFlightData:
    """This class is responsible for holding and structuring the cheapest flight data."""
    def __init__(self,cheapest_flight_data,flight_return_date):
        self.price = cheapest_flight_data.get("price")
        self.departure_date = cheapest_flight_data.get("flights", "N/A")[0].get("departure_airport", "N/A").get("time", "N/A").split(" ")[0]
        self.return_date = flight_return_date
        self.airline = cheapest_flight_data.get("flights", "N/A")[0].get("airline", "N/A")