"""
main.py - Smart Bus Ticket Booking & Reservation System (console version).

This is the program you run:   python3 main.py

It shows a menu, reads the user's choice with input(), and calls the
rules in core.py. It uses only built-in Python - nothing to install.
"""

from core import ReservationSystem

MENU = """
SMART BUS RESERVATION SYSTEM
================================
1. View Available Routes
2. Search for a Route
3. Book a Ticket
4. View My Bookings
5. Cancel a Booking
6. View Seat Availability
7. Generate Booking Report
8. Exit
================================"""


# ---------- Option 1 ----------
def view_routes(system):
    print("\nAVAILABLE BUS ROUTES")
    print(f"{'No.':<4} {'Route':<6} {'Journey':<26} {'Depart':<9} {'Fare':<9} {'Seats':<7} Status")
    # enumerate() gives us a counter (1, 2, 3...) together with each route
    for number, route in enumerate(system.routes, start=1):
        journey = f"{route['departure']} -> {route['destination']}"
        seats = f"{route['available_seats']}/{route['total_seats']}"
        status = system.availability_status(route)
        print(f"{number:<4} {route['route_id']:<6} {journey:<26} {route['departure_time']:<9} "
              f"Rs.{route['fare']:<6} {seats:<7} {status}")


# ---------- Option 2 ----------
def search_route(system):
    term = input("Search by route ID or city: ").strip()
    if not term:
        print("Please type a route ID (e.g. R101) or a city (e.g. Karachi).")
        return
    matches = system.search(term)
    if not matches:
        print(f"No routes found for '{term}'.")
        return
    for route in matches:
        print(f"{route['route_id']} | {route['departure']} -> {route['destination']} | "
              f"{route['departure_time']} | Rs. {route['fare']} | "
              f"{route['available_seats']} seats available")


# ---------- Option 3 ----------
def book_ticket(system):
    print("\nBOOK A TICKET")
    name = input("Passenger name: ")
    age = input("Passenger age: ")
    route_id = input("Route ID (e.g. R101): ")
    seats = input("Number of seats: ")
    try:
        booking = system.book(name, age, route_id, seats)
    except ValueError as error:
        # Something was wrong. core.py changed nothing, so we just explain why.
        print(f"Booking failed: {error}")
        return
    route = system.find_route(booking["route_id"])
    print("\nBooking confirmed!")
    print(f"Booking ID: {booking['booking_id']}")
    print(f"Passenger: {booking['passenger_name']}")
    print(f"Route: {route['route_id']} ({route['departure']} -> {route['destination']})")
    print(f"Seats booked: {booking['seats']}")
    print(f"Fare per seat: Rs. {route['fare']}")
    print(f"Total fare: Rs. {booking['total_fare']}")
    print(f"Status: {booking['status']}")


# ---------- Option 4 ----------
def view_bookings(system):
    if not system.bookings:
        print("No bookings found.")
        return
    print("\nMY BOOKINGS")
    print(f"{'No.':<4} {'ID':<7} {'Passenger':<15} {'Age':<4} {'Route':<6} {'Seats':<6} {'Fare':<10} Status")
    for number, booking in enumerate(system.bookings, start=1):
        print(f"{number:<4} {booking['booking_id']:<7} {booking['passenger_name'][:15]:<15} "
              f"{booking['passenger_age']:<4} {booking['route_id']:<6} {booking['seats']:<6} "
              f"Rs.{booking['total_fare']:<7} {booking['status']}")


# ---------- Option 5 ----------
def cancel_booking(system):
    booking_id = input("Enter booking ID to cancel: ")
    try:
        booking, route = system.cancel(booking_id)
    except ValueError as error:
        print(f"Cancellation failed: {error}")
        return
    print(f"Booking {booking['booking_id']} has been cancelled.")
    print(f"Seats restored: {booking['seats']}")
    print(f"Route {route['route_id']} available seats: {route['available_seats']}")


# ---------- Option 6 ----------
def view_seat_availability(system):
    answer = input("Show only routes with seats available? (y/n): ").strip().lower()
    only_available = answer in ("y", "yes")
    print("\nSEAT AVAILABILITY")
    print(f"{'Route':<6} {'Available/Total':<16} Status")
    shown = 0
    for route in system.routes:
        if only_available and route["available_seats"] == 0:
            continue                      # skip fully booked routes when filtering
        seats = f"{route['available_seats']}/{route['total_seats']}"
        print(f"{route['route_id']:<6} {seats:<16} {system.availability_status(route)}")
        shown += 1
    if shown == 0:
        print("No routes have seats available.")


# ---------- Option 7 ----------
def generate_report(system):
    totals = system.report()
    print("\nBOOKING REPORT")
    print(f"Total bookings created: {totals['total_bookings']}")
    print(f"Confirmed bookings: {totals['confirmed_bookings']}")
    print(f"Cancelled bookings: {totals['cancelled_bookings']}")
    print(f"Seats currently reserved: {totals['seats_reserved']}")
    print(f"Confirmed revenue: Rs. {totals['revenue']:,}")
    print(f"Fully booked routes: {totals['fully_booked_routes']}")

    print("\nCONFIRMED BOOKINGS BY ROUTE")
    for row in system.report_by_route():
        print(f"  {row['route_id']}: {row['seats']} seat(s), Rs. {row['revenue']:,}")

    show_schedule(system)


def show_schedule(system):
    print("\nROUTE SCHEDULE BY DEPARTURE CITY")
    for city, routes in system.schedule().items():
        print(city)
        if not routes:
            print("  No scheduled departures.")
        for route in routes:
            print(f"  {route['route_id']} -> {route['destination']:<12} | {route['departure_time']}")


# ---------- Main menu loop ----------
def main():
    system = ReservationSystem()
    print("Welcome to the Smart Bus Ticket Booking & Reservation System!")
    print("Note: bookings are kept in memory only and are lost when you exit.")

    while True:                               # keep showing the menu until Exit
        print(MENU)
        choice = input("Enter your choice: ").strip()

        if not choice.isdigit():
            print("Invalid choice. Please enter a number from 1 to 8.")
            continue                          # go back to the top of the loop

        choice = int(choice)
        if choice == 1:
            view_routes(system)
        elif choice == 2:
            search_route(system)
        elif choice == 3:
            book_ticket(system)
        elif choice == 4:
            view_bookings(system)
        elif choice == 5:
            cancel_booking(system)
        elif choice == 6:
            view_seat_availability(system)
        elif choice == 7:
            generate_report(system)
        elif choice == 8:
            print("Thank you for using Smart Bus. Goodbye!")
            break                             # leave the loop - program ends
        else:
            print("Invalid choice. Please enter a number from 1 to 8.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C or end of input: exit politely instead of showing an error
        print("\nProgram closed. Goodbye!")
