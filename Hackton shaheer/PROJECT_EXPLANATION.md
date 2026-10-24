# Project Explanation (in simple English)

## 1. What is this project?

It is a small program for a bus company. A person sits at the computer and uses a
**menu** (numbers 1 to 8) to:

- see bus routes
- search for a route
- book seats
- see bookings
- cancel a booking
- check how many seats are left
- see a report and the bus schedule

It runs in the **terminal** (black text window). There is no website or database.
Everything is stored in Python **lists** and **dictionaries** while the program is open.
When the program closes, the bookings are gone. The PRD asks for exactly this.

## 2. The files

| File | Simple explanation |
|---|---|
| `main.py` | **The face.** Shows the menu, asks questions with `input()`, prints answers with `print()`. |
| `core.py` | **The brain.** Stores routes and bookings and checks all the rules. It never prints anything. |
| `test_core.py` | Automatic checks that the brain follows every rule. |
| `test_main.py` | Automatic checks that run the real program and type answers, one per PRD test case. |
| `test_cases.txt` | The 12 PRD test cases with the real results. |
| `screenshots/` | Pictures of the real program: routes, booking, cancellation, report. |
| `gui.py` | Optional extra web page that uses the same brain (`core.py`). Not needed for the PRD. |

**Why two files (`main.py` and `core.py`)?**
Keeping the rules separate from the screen means the same rules work for the console *and*
for the optional web page. It also makes testing easy, because we can test the rules without typing.

## 3. The data (what we store)

### Routes: a list of dictionaries (`core.py`, `_STARTER_ROUTES`)

Each route is one dictionary:

```python
{"route_id": "R101", "departure": "Karachi", "destination": "Hyderabad",
 "departure_time": "08:00 AM", "fare": 1200, "total_seats": 40, "available_seats": 40}
```

There are 5 routes: R101 to R105. They are copied into `self.routes` when the program starts.

### Bookings: a list of dictionaries (`self.bookings`)

Each booking is one dictionary:

```python
{"booking_id": "B1001", "passenger_name": "Ahmed", "passenger_age": 24,
 "route_id": "R101", "seats": 2, "total_fare": 2400, "status": "Confirmed"}
```

`status` is either `"Confirmed"` or `"Cancelled"`. Cancelled bookings are **kept**, not deleted.

### Cities: a tuple (`SUPPORTED_CITIES`)

```python
("Karachi", "Hyderabad", "Sukkur", "Mirpur Khas", "Lahore")
```

A tuple is used because the list of cities never changes.

### Issued booking IDs: a set (`self.issued_ids`)

A set remembers every booking ID we have given out, like `{"B1001", "B1002"}`.
Before giving out a new ID we check it is not already in the set, so **IDs are never repeated**,
not even after a cancellation.

## 4. The functions in `core.py` (the brain)

All of them live inside the class `ReservationSystem`. A class is just a box that keeps the data
(routes, bookings, IDs) and the functions that work on that data together.

| Function | What it does |
|---|---|
| `__init__` | Runs at start. Makes the routes list, an empty bookings list, an empty ID set, and sets the next ID to 1001. |
| `find_route(route_id)` | Finds a route by its ID (e.g. `"r101"` finds R101). Returns `None` if not found. |
| `get_booking(booking_id)` | Finds a booking by its ID. Returns `None` if not found. |
| `search(term)` | First tries an exact route ID. If none, finds **all** routes where the city name matches (from or to). |
| `availability_status(route)` | Returns `"Available"`, `"Partially Booked"` or `"Fully Booked"`. |
| `book(name, age, route_id, seats)` | Checks everything, then creates the booking and reduces seats. |
| `cancel(booking_id)` | Checks the booking is Confirmed, sets it to Cancelled, gives the seats back. |
| `report()` | Counts bookings, seats and revenue (Confirmed only) and full routes. |
| `report_by_route()` | Seats and revenue for each route (nested loops). |
| `schedule()` | Groups routes by departure city (nested loops). |
| `to_positive_int(value, message)` | Helper: turns `"24"` into `24`; rejects text, decimals, zero and negatives. |

### How booking works (`book`), step by step

1. Name: remove spaces. If empty, **stop** with "Passenger name cannot be blank."
2. Age must be a whole number from 1 to 120, otherwise **stop**.
3. Route must exist, otherwise **stop**.
4. Seats must be a whole number of 1 or more, otherwise **stop**.
5. Seats must be no more than available seats, otherwise **stop**.
6. Make a new unique ID (B1001, B1002, ...) using the set.
7. Fare = ticket price × seats.
8. Save the booking **and only now** subtract the seats.

"Stop" means Python raises a `ValueError`. `main.py` catches it and prints
"Booking failed: ..." Because we stop **before** step 8, a failed booking changes nothing.

### How cancelling works (`cancel`)

1. Find the booking. Not found? Stop: "Booking ... not found."
2. Already cancelled? Stop: "Booking ... is already cancelled." (This prevents giving seats back twice.)
3. Set status to "Cancelled" and add the seats back to the route **once**.
4. The booking stays in the list so it still appears in history and reports.

### How the report works (`report`)

- **Total bookings** = every booking (confirmed + cancelled).
- **Confirmed / Cancelled** = counted by status.
- **Seats reserved** and **revenue** = added up from **Confirmed bookings only**.
- **Fully booked routes** = routes with 0 seats left.

## 5. The functions in `main.py` (the face)

| Function | Menu option |
|---|---|
| `view_routes` | 1: prints the numbered route table |
| `search_route` | 2: asks for a search word and prints matches or "No routes found" |
| `book_ticket` | 3: asks 4 questions, calls `book`, prints the confirmation or the error |
| `view_bookings` | 4: numbered list of all bookings or "No bookings found." |
| `cancel_booking` | 5: asks for an ID, calls `cancel`, prints seats restored |
| `view_seat_availability` | 6: asks y/n for the filter, prints status for each route |
| `generate_report` | 7: prints totals, per-route numbers, then calls `show_schedule` |
| `show_schedule` | Prints routes grouped by departure city |
| `main` | The menu loop: shows the menu, reads the choice, runs the option, repeats until 8 |

The **route schedule** is shown at the end of option 7, so the menu keeps the exact 8 options from the PRD.

## 6. How invalid input is handled

- Menu: anything that is not a number (e.g. `abc`) or not 1–8 (e.g. `99`) prints
  "Invalid choice. Please enter a number from 1 to 8." and shows the menu again.
- Booking and cancelling: errors are printed as "Booking failed: ..." or
  "Cancellation failed: ...". The program never crashes.
- Pressing Ctrl+C closes the program politely.

## 7. Testing

- `python3 -m unittest -v` runs **32 automatic tests**.
- They passed on macOS (Python 3.14 and 3.9) and on Linux (Debian, Python 3.12 in Docker).
- `test_cases.txt` lists the 12 PRD test cases with the real results.

## 8. Limitations (be honest about these)

- No saving: data is lost when the program closes (the PRD asks for this).
- One user at a time, no login (the PRD says login is not needed).
- Seat numbers (like "seat 12A") are not tracked, only how many seats are booked.
