"""
Runs the real console program (main.py) with typed-in answers and checks
what it prints. One test for each of the 12 PRD test cases (TC-01 to TC-12).
Run with:   python3 -m unittest -v
"""

import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))


def run_program(*answers):
    """Start main.py, type each answer followed by Enter, return everything it printed."""
    typed = "\n".join(answers) + "\n"
    result = subprocess.run(
        [sys.executable, "main.py"], input=typed, capture_output=True,
        text=True, cwd=HERE, timeout=20,
    )
    return result.stdout + result.stderr


BOOK_AHMED = ["3", "Ahmed", "24", "R101", "2"]


class TestPRDScenarios(unittest.TestCase):
    def test_tc01_view_all_routes(self):
        out = run_program("1", "8")
        for route_id in ("R101", "R102", "R103", "R104", "R105"):
            self.assertIn(route_id, out)
        self.assertIn("40/40", out)
        self.assertIn("Available", out)

    def test_tc02_search_hyderabad(self):
        out = run_program("2", "Hyderabad", "8")
        self.assertIn("R101 | Karachi -> Hyderabad", out)
        self.assertIn("R103 | Hyderabad -> Mirpur Khas", out)
        self.assertIn("R105 | Sukkur -> Hyderabad", out)
        self.assertNotIn("R102 |", out)

    def test_tc03_unknown_city(self):
        out = run_program("2", "Atlantis", "8")
        self.assertIn("No routes found for 'Atlantis'.", out)
        self.assertIn("Goodbye", out)            # program kept running and exited normally

    def test_tc04_book_two_seats(self):
        out = run_program(*BOOK_AHMED, "1", "8")
        self.assertIn("Booking ID: B1001", out)
        self.assertIn("Total fare: Rs. 2400", out)
        self.assertIn("38/40", out)

    def test_tc05_zero_seats(self):
        out = run_program("3", "Ahmed", "24", "R101", "0", "4", "1", "8")
        self.assertIn("Booking failed: Seat quantity must be a positive whole number.", out)
        self.assertIn("No bookings found.", out)
        self.assertIn("40/40", out)

    def test_tc06_too_many_seats(self):
        out = run_program("3", "Ahmed", "24", "R101", "41", "1", "8")
        self.assertIn("Booking failed: Only 40 seat(s) available on R101.", out)
        self.assertIn("40/40", out)

    def test_tc07_cancel_confirmed_booking(self):
        out = run_program(*BOOK_AHMED, "5", "B1001", "4", "8")
        self.assertIn("Booking B1001 has been cancelled.", out)
        self.assertIn("Seats restored: 2", out)
        self.assertIn("Route R101 available seats: 40", out)
        self.assertIn("Cancelled", out)          # still visible in history

    def test_tc08_cancel_same_booking_again(self):
        out = run_program(*BOOK_AHMED, "5", "B1001", "5", "B1001", "6", "n", "8")
        self.assertIn("Cancellation failed: Booking B1001 is already cancelled.", out)
        self.assertIn("40/40", out)              # not 42/40
        self.assertNotIn("42/40", out)

    def test_tc09_report_with_no_bookings(self):
        out = run_program("7", "8")
        self.assertIn("Total bookings created: 0", out)
        self.assertIn("Confirmed revenue: Rs. 0", out)
        self.assertIn("Fully booked routes: 0", out)
        self.assertIn("No scheduled departures.", out)

    def test_tc10_book_all_seats(self):
        out = run_program("3", "Sara", "30", "R105", "30", "6", "n", "7", "8")
        self.assertIn("Booking confirmed!", out)
        self.assertIn("0/30", out)
        self.assertIn("Fully Booked", out)
        self.assertIn("Fully booked routes: 1", out)

    def test_tc11_report_after_cancellation(self):
        out = run_program(*BOOK_AHMED, "3", "Sara", "30", "R103", "3", "5", "B1001", "7", "8")
        self.assertIn("Total bookings created: 2", out)
        self.assertIn("Confirmed bookings: 1", out)
        self.assertIn("Cancelled bookings: 1", out)
        self.assertIn("Seats currently reserved: 3", out)
        self.assertIn("Confirmed revenue: Rs. 2,400", out)   # only Sara's 3 x 800

    def test_tc12_invalid_menu_option(self):
        out = run_program("abc", "99", "", "0", "8")
        self.assertEqual(out.count("Invalid choice. Please enter a number from 1 to 8."), 4)
        self.assertIn("Goodbye", out)

    def test_end_of_input_does_not_crash(self):
        out = run_program("1")                    # no "8" - input simply ends
        self.assertIn("Program closed. Goodbye!", out)
        self.assertNotIn("Traceback", out)


if __name__ == "__main__":
    unittest.main()
