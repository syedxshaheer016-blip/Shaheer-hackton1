# Python Concepts Used (and where to find them)

Each concept has a short meaning, the real code from this project, and where it is.
Line numbers can move a little if the code is edited, so the function name is the best guide.

---

## 1. `print()` and `input()`
**Meaning:** `print()` shows text; `input()` waits for the user to type and press Enter.
**Where:** `main.py`, function `main()`, plus every menu function.

```python
choice = input("Enter your choice: ").strip()
print("Invalid choice. Please enter a number from 1 to 8.")
```

## 2. Variables and data types
**Meaning:** A variable is a named box holding a value.
- **String** (text): `"R101"`, `"Confirmed"`, passenger names
- **Integer** (whole number): age `24`, seats `2`, fare `1200`
- **Boolean** (True/False): `only_available = answer in ("y", "yes")` in `main.py` → `view_seat_availability()`

**Where:** everywhere, e.g. `core.py` → `book()`:

```python
"total_fare": route["fare"] * seats,
```

## 3. Lists
**Meaning:** An ordered collection that can grow.
**Where:** `core.py` → `__init__()`: routes and bookings are lists.

```python
self.bookings = []          # starts empty
self.bookings.append(booking)   # in book(): add a new booking to the end
```

**Why:** we have many routes and many bookings, in order.

## 4. Dictionaries
**Meaning:** Values stored under names (keys), like a form with labels.
**Where:** each route (`_STARTER_ROUTES` at the top of `core.py`) and each booking (`book()`).

```python
booking = {"booking_id": booking_id, "passenger_name": name, "seats": seats, "status": "Confirmed", ...}
```

**Why:** `booking["status"]` is much clearer than "item number 6".

## 5. Tuples
**Meaning:** Like a list, but it **cannot be changed**.
**Where:** `core.py`, near the top:

```python
SUPPORTED_CITIES = ("Karachi", "Hyderabad", "Sukkur", "Mirpur Khas", "Lahore")
```

**Why:** the city list is fixed, so a tuple protects it from accidental changes.

## 6. Sets
**Meaning:** A collection with **no duplicates** and very fast "is it inside?" checks.
**Where:** `core.py` → `__init__()` and `book()`:

```python
self.issued_ids = set()
...
if booking_id not in self.issued_ids:
    self.issued_ids.add(booking_id)
    break
```

**Why:** guarantees every booking ID is unique (PRD rule BR-06).

## 7. `if`, `elif`, `else`
**Meaning:** Choose what to do depending on a condition.
**Where:** `main.py` → `main()` chooses the menu action; `core.py` → `availability_status()`:

```python
if route["available_seats"] == 0:
    return "Fully Booked"
elif route["available_seats"] == route["total_seats"]:
    return "Available"
else:
    return "Partially Booked"
```

## 8. Nested conditions
**Meaning:** Checks one after another, each only if the previous passed.
**Where:** `core.py` → `book()` checks name → age → route → seats → enough seats,
and `cancel()` checks found → not already cancelled → route exists.

## 9. `for` loops
**Meaning:** Repeat something for every item in a list.
**Where:** `core.py` → `report()` visits every booking:

```python
for booking in self.bookings:
    if booking["status"] == "Confirmed":
        confirmed += 1
        seats_reserved += booking["seats"]
        revenue += booking["total_fare"]
    else:
        cancelled += 1
```

## 10. Nested `for` loops (a loop inside a loop)
**Where 1:** `core.py` → `schedule()` (route schedule, PRD Feature 10)

```python
for city in SUPPORTED_CITIES:          # outer loop: every city
    departures = []
    for route in self.routes:          # inner loop: every route
        if route["departure"].lower() == city.lower():
            departures.append(route)
    result[city] = departures
```

**Where 2:** `core.py` → `report_by_route()`: outer loop over routes, inner loop over bookings
(PRD Feature 9).

## 11. `for-else`
**Meaning:** The `else` part runs **only if the loop finished without `break`**, which means
"we looked at everything and did not find it".
**Where:** `core.py` → `find_route()`, `get_booking()` and `search()`:

```python
for route in self.routes:
    if route["route_id"] == wanted:
        break            # found it - stop looking
else:
    return None          # loop ended WITHOUT break: no route matched
return route
```

In `search()`, the `else` means "no route ID matched, so search by city instead".

## 12. `break`
**Meaning:** Leave a loop immediately.
**Where:**
- `main.py` → `main()`: option 8 → `break` ends the menu loop and the program.
- `core.py` → `find_route()` / `get_booking()` / `search()`: stop once the unique ID is found.
- `core.py` → `book()`: stop the ID loop once a free ID is found.

## 13. `continue`
**Meaning:** Skip the rest of this round and jump to the next round of the loop.
**Where:**
- `main.py` → `main()`: after an invalid menu choice, `continue` shows the menu again.
- `main.py` → `view_seat_availability()`: skip fully booked routes when the filter is on:

```python
if only_available and route["available_seats"] == 0:
    continue
```

- `core.py` → `report_by_route()`: skip bookings for other routes or cancelled ones.

## 14. `enumerate()`
**Meaning:** Gives a counter **and** the item at the same time.
**Where:** `main.py` → `view_routes()` and `view_bookings()`:

```python
for number, route in enumerate(system.routes, start=1):
```

**Why:** to print the numbers 1, 2, 3... in front of each row.

## 15. `while` loop
**Meaning:** Repeat while something is true.
**Where:** `main.py` → `main()`: `while True:` keeps showing the menu until `break` (option 8).
Also `core.py` → `book()` uses `while True:` to find a free booking ID.

## 16. Fare calculation
**Where:** `core.py` → `book()`: `route["fare"] * seats`. Example: 1200 × 2 = 2400.

## 17. Input validation and `try` / `except`
**Meaning:** `try` runs code that might fail; `except` catches the error instead of crashing.
**Where:** `core.py` → `to_positive_int()`:

```python
try:
    number = int(str(value).strip())
except ValueError:
    raise ValueError(message)
```

`main.py` → `book_ticket()` catches the error and prints "Booking failed: ...".

## 18. Functions and a class (bonus)
**Meaning:** A function is a named block of code you can reuse. A class groups data and
functions together. `ReservationSystem` holds routes, bookings and IDs, plus the functions that change them.
