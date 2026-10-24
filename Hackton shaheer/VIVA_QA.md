# Viva Questions & Answers

Short answers you can remember. The file or function to point at is shown in brackets.

## About the project

**1. What does your project do?**
It is a bus ticket booking system in the terminal. You can view and search routes, book and cancel
tickets, check seats, and see a report with the schedule.

**2. Which language and libraries did you use?**
Python 3, built-in features only. No external libraries for the main program.

**3. How do I run it?**
`python3 main.py` inside the `smart-bus-hackathon` folder.

**4. Why are there two main files?**
`main.py` is the screen (menu, input, print). `core.py` is the brain (data and rules). Keeping them
apart makes the rules easy to test and reuse.

**5. Where is the data saved?**
Only in memory, in lists and dictionaries. When the program closes, bookings are lost. The PRD asks
for no database.

## Data structures

**6. How are routes stored?**
As a list of dictionaries. Each dictionary is one route with ID, cities, time, fare, total seats and
available seats. (`core.py`, `_STARTER_ROUTES`)

**7. How are bookings stored?**
As a list of dictionaries in `self.bookings`. Each one has ID, name, age, route, seats, total fare and status.

**8. Why use a dictionary for a booking?**
Because named fields like `booking["status"]` are clear and easy to read.

**9. Where do you use a tuple, and why?**
`SUPPORTED_CITIES`. The cities never change, and a tuple cannot be changed.

**10. Where do you use a set, and why?**
`issued_ids` remembers every booking ID given out. A set has no duplicates and checks fast,
so IDs are always unique.

## Booking

**11. How is the booking ID made?**
A counter starts at 1001, so the IDs are B1001, B1002 and so on. Each new ID is checked against the set
before use. (`core.py`, `book`)

**12. Can a booking ID be reused after a cancellation?**
No. The counter only goes up and the set remembers all old IDs.

**13. How is the fare calculated?**
Ticket price × number of seats. Example: 1200 × 2 = 2400.

**14. What checks happen before booking?**
Name not blank; age a whole number from 1 to 120; route exists; seats a whole number of 1 or more;
seats not more than available.

**15. What happens if one check fails?**
`core.py` raises a `ValueError`. `main.py` catches it and prints "Booking failed: …".
Nothing is changed.

**16. How do you prevent overbooking?**
Before booking we check `seats > route["available_seats"]`. If true, the booking is rejected.
Seats can never go below zero.

**17. When are seats reduced?**
Only at the very end, after every check has passed.

## Cancellation

**18. How does cancelling work?**
Find the booking. If it is Confirmed, change its status to Cancelled and add its seats back to the route.

**19. How do you stop seats being restored twice?**
If the status is already Cancelled, we reject the request before touching the seats.

**20. Why not delete a cancelled booking?**
The PRD wants history. Cancelled bookings stay visible in option 4 and are counted in the report.

## Reports and schedule

**21. Is cancelled money counted as revenue?**
No. Revenue and reserved seats only add up Confirmed bookings.

**22. What does the report show when there are no bookings?**
All zeros, and it still counts fully booked routes (0 at the start).

**23. Where do you use nested loops?**
In `schedule()`: the outer loop is over cities and the inner loop over routes. Also in
`report_by_route()`: the outer loop is over routes and the inner loop over bookings.

**24. Where is the route schedule in the menu?**
At the end of option 7 (Generate Booking Report), so the menu keeps the PRD's 8 options.

## Python concepts

**25. Where do you use `for-else`?**
In `find_route`, `get_booking` and `search`. The `else` runs only if the loop did **not** `break`,
which means nothing was found.

**26. Where do you use `break`?**
Option 8 breaks the menu loop. Searches break once the unique ID is found. The ID loop breaks once
a free ID is found.

**27. Where do you use `continue`?**
In the menu after an invalid choice; in seat availability to skip full routes; in
`report_by_route` to skip other routes and cancelled bookings.

**28. Where do you use `enumerate()`?**
In `view_routes` and `view_bookings`, to print row numbers 1, 2, 3…

**29. Why `while True` for the menu?**
The menu must repeat until the user chooses Exit. Option 8 uses `break` to stop it.

**30. What happens if I type `abc` in the menu?**
`isdigit()` is false, so it prints "Invalid choice. Please enter a number from 1 to 8." and `continue`
shows the menu again.

**31. What if I type `2.5` or `abc` as the age?**
`int()` fails inside `try`, so we raise "Age must be a positive whole number." and nothing changes.

## Testing

**32. How did you test it?**
32 automatic tests with Python's built-in `unittest`. They cover all rules and all 12 PRD test cases.
Run them with `python3 -m unittest -v`. The results are written in `test_cases.txt`.

**33. Did it work on Linux?**
Yes. All 32 tests passed on Linux (Debian 13, Python 3.12, in Docker) and on macOS
(Python 3.14 and 3.9).

**34. What is `gui.py`?**
An optional web version using the NiceGUI library. It uses the same rules from `core.py`. It is
extra, not part of the PRD.

**35. What would you improve next?**
Optional PRD features: a 10% discount for 4+ seats, search by passenger name, and saving data to a
file.
