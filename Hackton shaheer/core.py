"""
core.py - the "brain" of the Smart Bus Reservation System.

This file holds all the DATA (routes and bookings) and all the RULES
(validation, booking, cancellation, reports). It does not print anything
and does not ask the user anything - main.py (console) and gui.py (web)
do that and call the functions here.

Everything is kept in memory (lists and dictionaries). When the program
closes, all bookings are lost. This is what the PRD asks for.
"""

from copy import deepcopy

# LIST of DICTIONARIES: one dictionary per bus route (PRD Feature 2).
_STARTER_ROUTES = [
    {"route_id": "R101", "departure": "Karachi", "destination": "Hyderabad",
     "departure_time": "08:00 AM", "fare": 1200, "total_seats": 40, "available_seats": 40},
    {"route_id": "R102", "departure": "Karachi", "destination": "Sukkur",
     "departure_time": "09:30 AM", "fare": 2000, "total_seats": 36, "available_seats": 36},
    {"route_id": "R103", "departure": "Hyderabad", "destination": "Mirpur Khas",
     "departure_time": "11:00 AM", "fare": 800, "total_seats": 32, "available_seats": 32},
    {"route_id": "R104", "departure": "Karachi", "destination": "Lahore",
     "departure_time": "07:00 PM", "fare": 5000, "total_seats": 45, "available_seats": 45},
    {"route_id": "R105", "departure": "Sukkur", "destination": "Hyderabad",
     "departure_time": "02:00 PM", "fare": 1500, "total_seats": 30, "available_seats": 30},
]

# TUPLE: the list of cities never changes, so a tuple is the right choice.
SUPPORTED_CITIES = ("Karachi", "Hyderabad", "Sukkur", "Mirpur Khas", "Lahore")

MAX_AGE = 120


def to_positive_int(value, message):
    """Turn text like '24' into the number 24.

    Rejects text ('abc'), decimals ('2.5'), zero and negative numbers by
    raising ValueError with the given message.
    """
    try:
        number = int(str(value).strip())   # str() first, so True or 2.9 are rejected too
    except ValueError:
        raise ValueError(message)
    if number <= 0:
        raise ValueError(message)
    return number


class ReservationSystem:
    """All state and rules for the reservation workflow."""

    def __init__(self):
        self.routes = deepcopy(_STARTER_ROUTES)  # fresh copy of the 5 starter routes
        self.bookings = []                       # LIST of booking dictionaries
        self.issued_ids = set()                  # SET of booking IDs already given out
        self._next_id = 1001                     # first booking ID will be B1001

    # ---------- finding things ----------
    def find_route(self, route_id):
        """Return the route dictionary for a route ID, or None if it does not exist."""
        wanted = str(route_id).strip().upper()
        for route in self.routes:
            if route["route_id"] == wanted:
                break            # found it - stop looking
        else:
            return None          # for-else: loop ended WITHOUT break, so no route matched
        return route

    def get_booking(self, booking_id):
        """Return the booking dictionary for a booking ID, or None if it does not exist."""
        wanted = str(booking_id).strip().upper()
        for booking in self.bookings:
            if booking["booking_id"] == wanted:
                break
        else:
            return None          # for-else: no booking had this ID
        return booking

    def search(self, term):
        """Search by route ID (exact) or by city name (departure or destination).

        Returns a list of matching routes. An empty list means "no match".
        """
        text = str(term).strip().lower()
        matches = []
        if not text:
            return matches

        # 1) Route IDs are unique, so we can stop (break) at the first match.
        for route in self.routes:
            if route["route_id"].lower() == text:
                matches.append(route)
                break
        else:
            # 2) for-else: no route ID matched, so search by city and keep ALL matches.
            for route in self.routes:
                if text in route["departure"].lower() or text in route["destination"].lower():
                    matches.append(route)
        return matches

    def availability_status(self, route):
        """Return 'Available', 'Partially Booked' or 'Fully Booked' (PRD Feature 8)."""
        if route["available_seats"] == 0:
            return "Fully Booked"
        elif route["available_seats"] == route["total_seats"]:
            return "Available"
        else:
            return "Partially Booked"

    # ---------- changing things ----------
    def book(self, name, age, route_id, seats):
        """Create a Confirmed booking. Raises ValueError if any check fails.

        All checks happen FIRST. Seats are only changed after every check passes,
        so a failed booking never changes anything (PRD BR-01 to BR-08).
        """
        name = str(name).strip()
        if not name:
            raise ValueError("Passenger name cannot be blank.")

        age = to_positive_int(age, "Age must be a positive whole number.")
        if age > MAX_AGE:
            raise ValueError(f"Age must be between 1 and {MAX_AGE}.")

        route = self.find_route(route_id)
        if route is None:
            raise ValueError(f"Route '{str(route_id).strip()}' does not exist.")

        seats = to_positive_int(seats, "Seat quantity must be a positive whole number.")
        if seats > route["available_seats"]:
            raise ValueError(
                f"Only {route['available_seats']} seat(s) available on {route['route_id']}."
            )

        # Make a unique booking ID. The set tells us which IDs were already used,
        # so even cancelled IDs are never given out again.
        while True:
            booking_id = f"B{self._next_id}"
            self._next_id += 1
            if booking_id not in self.issued_ids:
                self.issued_ids.add(booking_id)
                break

        booking = {
            "booking_id": booking_id,
            "passenger_name": name,
            "passenger_age": age,
            "route_id": route["route_id"],
            "seats": seats,
            "total_fare": route["fare"] * seats,   # fare = ticket price x seats
            "status": "Confirmed",
        }
        self.bookings.append(booking)
        route["available_seats"] -= seats          # update seats only after all checks passed
        return booking

    def cancel(self, booking_id):
        """Cancel a Confirmed booking and give its seats back (only once).

        Returns (booking, route). Raises ValueError if it cannot be cancelled.
        The booking is NOT deleted - it stays in history with status 'Cancelled'.
        """
        booking = self.get_booking(booking_id)
        if booking is None:
            raise ValueError(f"Booking '{str(booking_id).strip()}' not found.")
        if booking["status"] == "Cancelled":
            raise ValueError(f"Booking {booking['booking_id']} is already cancelled.")

        route = self.find_route(booking["route_id"])
        if route is None:
            raise ValueError("Route data missing for this booking.")

        booking["status"] = "Cancelled"
        route["available_seats"] += booking["seats"]   # restore exactly once
        return booking, route

    # ---------- reports ----------
    def report(self):
        """Totals for the booking report (PRD Feature 9). Cancelled bookings earn no revenue."""
        confirmed = 0
        cancelled = 0
        seats_reserved = 0
        revenue = 0
        for booking in self.bookings:
            if booking["status"] == "Confirmed":
                confirmed += 1
                seats_reserved += booking["seats"]
                revenue += booking["total_fare"]
            else:
                cancelled += 1

        fully_booked = 0
        for route in self.routes:
            if route["available_seats"] == 0:
                fully_booked += 1

        return {
            "total_bookings": len(self.bookings),
            "confirmed_bookings": confirmed,
            "cancelled_bookings": cancelled,
            "seats_reserved": seats_reserved,
            "revenue": revenue,
            "fully_booked_routes": fully_booked,
        }

    def report_by_route(self):
        """Confirmed seats and revenue for each route, using NESTED loops.

        Outer loop: every route. Inner loop: every booking for that route.
        """
        rows = []
        for route in self.routes:                  # outer loop
            seats = 0
            revenue = 0
            for booking in self.bookings:          # inner loop
                if booking["route_id"] != route["route_id"]:
                    continue                       # not this route - skip it
                if booking["status"] != "Confirmed":
                    continue                       # cancelled - skip it
                seats += booking["seats"]
                revenue += booking["total_fare"]
            rows.append({"route_id": route["route_id"], "seats": seats, "revenue": revenue})
        return rows

    def schedule(self):
        """City -> list of routes leaving that city, using NESTED loops (PRD Feature 10)."""
        result = {}
        for city in SUPPORTED_CITIES:              # outer loop: every city
            departures = []
            for route in self.routes:              # inner loop: every route
                if route["departure"].lower() == city.lower():
                    departures.append(route)
            result[city] = departures
        return result
