# Smart Bus Ticket Booking & Reservation System

A simple **Python 3 console program** for a small bus company. You can view bus routes,
search for a route, book seats, see your bookings, cancel a booking, check seat
availability, and print a report with the route schedule.

It was built from the *Smart Bus Ticket Booking PRD*. The main program (`main.py`)
uses **only built-in Python**, so there is nothing to install.

## What you need

- Python 3.9 or newer (tested with 3.9, 3.12 and 3.14)
- Works on macOS, Linux and Windows

Check your version:

```bash
python3 --version
```

## How to run

```bash
cd smart-bus-hackathon
python3 main.py
```

(On Windows, type `python` instead of `python3`.)

## Menu guide

| Option | What it does |
|---|---|
| 1. View Available Routes | Shows all 5 routes, their time, fare, seats left and status |
| 2. Search for a Route | Type a route ID (`R101`) or a city (`Hyderabad`) |
| 3. Book a Ticket | Enter name, age, route ID and number of seats; you get a booking ID |
| 4. View My Bookings | Lists every booking, including cancelled ones |
| 5. Cancel a Booking | Type a booking ID (`B1001`); the seats go back to the route |
| 6. View Seat Availability | Shows Available / Partially Booked / Fully Booked; can hide full routes |
| 7. Generate Booking Report | Totals, revenue, bookings per route, and the **route schedule** by city |
| 8. Exit | Closes the program |

## Sample workflow

1. Choose `1` to see the routes.
2. Choose `3` and book: `Ahmed`, `24`, `R101`, `2`. You get **B1001**, total **Rs. 2400**.
3. Choose `5` and cancel `B1001`. 2 seats go back to R101.
4. Choose `7` to see the report. The cancelled booking earns **no** revenue.
5. Choose `8` to exit.

`DEMO_SCRIPT.md` has a full step-by-step demo.

## How to run the tests

```bash
cd smart-bus-hackathon
python3 -m unittest -v
```

This runs 32 automated tests (business rules plus all 12 PRD test cases). The results are written up in
`test_cases.txt`.

## Important limitation: no saving

All routes and bookings are kept **in memory only** (Python lists and dictionaries).
When you close the program, **all bookings are lost**. The PRD asks for this; there is
no database and no file saving.

## Files

| File | Purpose |
|---|---|
| `main.py` | The console program: menu, questions and printing |
| `core.py` | The rules and data: routes, booking, cancelling, reports |
| `test_core.py` | Automated tests for the rules in `core.py` |
| `test_main.py` | Automated tests that run `main.py` for the 12 PRD test cases |
| `test_cases.txt` | The 12 PRD test cases with real results |
| `screenshots/` | The 4 PRD screenshots: routes, booking, cancellation, report |
| `gui.py` | *Optional* web version (needs an extra library, see below) |
| `PROJECT_EXPLANATION.md` | How the project works, in simple English |
| `DEMO_SCRIPT.md` | What to type during the presentation |
| `VIVA_QA.md` | Likely reviewer questions with short answers |
| `PYTHON_CONCEPTS.md` | Where each required Python concept is used |

## Optional: web version (not part of the PRD)

`gui.py` is an extra web interface built with the NiceGUI library. It uses the
same rules from `core.py`. It is **not required** by the PRD, which asks for a console app.

Use **Python 3.10 to 3.13** for the web version. It was tested with Python 3.12 + NiceGUI 3.18
on Linux. On Python 3.14, `pip` installed an old, broken NiceGUI/pydantic combination when tested.

```bash
cd smart-bus-hackathon
python3.12 -m venv .venv         # or python3.13 / python3.11 / python3.10
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install nicegui
python gui.py                    # then open http://127.0.0.1:8080
```
