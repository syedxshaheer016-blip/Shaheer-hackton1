# Demo Script (3–5 minutes)

Type exactly what is in the **Type** column. The **You should see** text is the real output of
the program. After each step the menu appears again; it is not repeated here.

> Tip: practise once before the presentation. Start fresh (close and reopen the program)
> so that the first booking ID is **B1001**.

## Before you start (say this, ~20 seconds)

> "This is a Smart Bus Ticket Booking system written in Python 3 using only built-in Python.
> `main.py` is the menu and screen. `core.py` holds the data and the rules.
> Routes and bookings are stored in lists and dictionaries in memory, so they disappear when
> the program closes. That is what the PRD asks for."

## Start the program

```bash
cd smart-bus-hackathon
python3 main.py
```

You should see the welcome message and the menu with options 1–8.

---

## Step 1: View routes (TC-01)

| Type | You should see |
|---|---|
| `1` | A numbered table of the 5 routes R101–R105, all `Available` |

```
1    R101   Karachi -> Hyderabad       08:00 AM  Rs.1200   40/40   Available
...
5    R105   Sukkur -> Hyderabad        02:00 PM  Rs.1500   30/30   Available
```

**Say:** "The numbers 1 to 5 come from `enumerate()`. Each route is a dictionary inside a list."

## Step 2: Search by city (TC-02)

| Type | You should see |
|---|---|
| `2` then `Hyderabad` | R101, R103 and R105 (to or from Hyderabad) |

**Say:** "Search ignores capital letters. It first checks route IDs, and if none match, the
`for-else` switches to searching by city and shows all matches."

## Step 3: Search for an unknown city (TC-03)

| Type | You should see |
|---|---|
| `2` then `Atlantis` | `No routes found for 'Atlantis'.` |

**Say:** "No crash. A helpful message, and the menu comes back."

## Step 4: Book a ticket (TC-04)

| Type | You should see |
|---|---|
| `3`, then `Ahmed`, `24`, `R101`, `2` | The booking confirmation |

```
Booking confirmed!
Booking ID: B1001
Passenger: Ahmed
Route: R101 (Karachi -> Hyderabad)
Seats booked: 2
Fare per seat: Rs. 1200
Total fare: Rs. 2400
Status: Confirmed
```

**Say:** "Total fare is price times seats: 1200 × 2 = 2400. The booking ID is unique because we
check a **set** of used IDs. Seats are reduced only after all checks pass."

## Step 5: Invalid booking (TC-05)

| Type | You should see |
|---|---|
| `3`, then `Ali`, `20`, `R101`, `0` | `Booking failed: Seat quantity must be a positive whole number.` |

**Say:** "Zero seats is rejected and nothing changes: no booking and no seat change."

## Step 6: Book all remaining seats (TC-10)

| Type | You should see |
|---|---|
| `3`, then `Sara`, `30`, `R105`, `30` | `Booking ID: B1002` … `Total fare: Rs. 45000` |

## Step 7: Seat availability with filter (Feature 8)

| Type | You should see |
|---|---|
| `6` then `y` | R101 `38/40 Partially Booked`, R102–R104 `Available`; **R105 is hidden** because it is full |

**Say:** "With the filter on, `continue` skips fully booked routes."

## Step 8: View bookings (Feature 6)

| Type | You should see |
|---|---|
| `4` | Two numbered rows: B1001 Ahmed (Confirmed) and B1002 Sara (Confirmed) |

## Step 9: Cancel a booking (TC-07)

| Type | You should see |
|---|---|
| `5` then `B1001` | The three lines below |

```
Booking B1001 has been cancelled.
Seats restored: 2
Route R101 available seats: 40
```

## Step 10: Cancel the same booking again (TC-08)

| Type | You should see |
|---|---|
| `5` then `B1001` | `Cancellation failed: Booking B1001 is already cancelled.` |

**Say:** "Seats are given back only once. A cancelled booking cannot be cancelled again."

## Step 11: Report and schedule (TC-11, Feature 9, Feature 10)

| Type | You should see |
|---|---|
| `7` | The report, the per-route totals, then the schedule |

```
BOOKING REPORT
Total bookings created: 2
Confirmed bookings: 1
Cancelled bookings: 1
Seats currently reserved: 30
Confirmed revenue: Rs. 45,000
Fully booked routes: 1
```

Then `CONFIRMED BOOKINGS BY ROUTE` (only R105 has seats) and `ROUTE SCHEDULE BY DEPARTURE CITY`
(Mirpur Khas and Lahore say `No scheduled departures.`).

**Say:** "Ahmed's cancelled Rs. 2,400 is **not** in the revenue. The schedule uses a
**nested loop**: the outer loop goes over cities, the inner loop over routes."

## Step 12: Invalid menu choice (TC-12)

| Type | You should see |
|---|---|
| `abc` | `Invalid choice. Please enter a number from 1 to 8.` |

## Step 13: Exit

| Type | You should see |
|---|---|
| `8` | `Thank you for using Smart Bus. Goodbye!` |

**Say:** "Option 8 uses `break` to leave the `while` loop."

---

## Optional: show the automated tests (~20 seconds)

```bash
python3 -m unittest -v
```

You should see `Ran 32 tests` and `OK`.

**Say:** "These 32 tests check every rule and all 12 PRD test cases automatically."

## Screenshots

The four PRD screenshots (routes, booking, cancellation, report) are already in the
`screenshots/` folder. Open them if the live demo cannot run, for example if there's no laptop or the
projector fails.
