"""
Automated tests for the business rules in core.py.
Run with:   python3 -m unittest -v
Uses only the built-in unittest module.
"""

import unittest

from core import ReservationSystem


class TestRoutesAndSearch(unittest.TestCase):
    def setUp(self):
        self.system = ReservationSystem()   # fresh, empty system for every test

    def test_five_starter_routes_with_original_fares(self):
        fares = {route["route_id"]: route["fare"] for route in self.system.routes}
        self.assertEqual(fares, {"R101": 1200, "R102": 2000, "R103": 800, "R104": 5000, "R105": 1500})

    def test_search_city_is_case_insensitive_and_finds_all(self):
        ids = [route["route_id"] for route in self.system.search("hYdErAbAd")]
        self.assertEqual(ids, ["R101", "R103", "R105"])

    def test_search_route_id_returns_one(self):
        ids = [route["route_id"] for route in self.system.search(" r104 ")]
        self.assertEqual(ids, ["R104"])

    def test_search_no_match_and_blank(self):
        self.assertEqual(self.system.search("Atlantis"), [])
        self.assertEqual(self.system.search("   "), [])

    def test_find_route_unknown(self):
        self.assertIsNone(self.system.find_route("R999"))


class TestBooking(unittest.TestCase):
    def setUp(self):
        self.system = ReservationSystem()

    def seats_left(self, route_id):
        return self.system.find_route(route_id)["available_seats"]

    def test_valid_booking(self):
        booking = self.system.book("Ahmed", "24", "r101", "2")
        self.assertEqual(booking["booking_id"], "B1001")
        self.assertEqual(booking["total_fare"], 2400)
        self.assertEqual(booking["status"], "Confirmed")
        self.assertEqual(self.seats_left("R101"), 38)

    def test_booking_ids_are_unique(self):
        ids = set()
        for _ in range(10):
            ids.add(self.system.book("A", 30, "R104", 1)["booking_id"])
        self.assertEqual(len(ids), 10)

    def test_invalid_inputs_change_nothing(self):
        bad_requests = [
            ("", 24, "R101", 1),          # blank name
            ("   ", 24, "R101", 1),       # whitespace name
            ("Ali", "abc", "R101", 1),    # text age
            ("Ali", 0, "R101", 1),        # zero age
            ("Ali", -5, "R101", 1),       # negative age
            ("Ali", "24.5", "R101", 1),   # decimal age
            ("Ali", 200, "R101", 1),      # unrealistic age
            ("Ali", True, "R101", 1),     # boolean is not an age
            ("Ali", 24, "R999", 1),       # unknown route
            ("Ali", 24, "R101", 0),       # zero seats
            ("Ali", 24, "R101", -2),      # negative seats
            ("Ali", 24, "R101", "two"),   # text seats
            ("Ali", 24, "R101", 2.9),     # decimal seats
            ("Ali", 24, "R101", 41),      # more seats than exist
        ]
        for request in bad_requests:
            with self.subTest(request=request):
                with self.assertRaises(ValueError):
                    self.system.book(*request)
        self.assertEqual(self.system.bookings, [])
        self.assertEqual(self.seats_left("R101"), 40)

    def test_overbooking_rejected_after_partial_booking(self):
        self.system.book("A", 30, "R105", 25)
        with self.assertRaises(ValueError):
            self.system.book("B", 30, "R105", 6)      # only 5 left
        self.assertEqual(self.seats_left("R105"), 5)

    def test_book_exactly_all_seats(self):
        self.system.book("A", 30, "R105", 30)
        route = self.system.find_route("R105")
        self.assertEqual(route["available_seats"], 0)
        self.assertEqual(self.system.availability_status(route), "Fully Booked")
        with self.assertRaises(ValueError):
            self.system.book("B", 30, "R105", 1)       # one more than available


class TestCancellation(unittest.TestCase):
    def setUp(self):
        self.system = ReservationSystem()
        self.booking = self.system.book("Ahmed", 24, "R101", 2)

    def test_cancel_restores_seats_once(self):
        booking, route = self.system.cancel("b1001")
        self.assertEqual(booking["status"], "Cancelled")
        self.assertEqual(route["available_seats"], 40)
        with self.assertRaises(ValueError):
            self.system.cancel("B1001")                # second cancel rejected
        self.assertEqual(route["available_seats"], 40)  # no extra seats

    def test_cancelled_booking_stays_in_history(self):
        self.system.cancel("B1001")
        self.assertEqual(len(self.system.bookings), 1)
        self.assertEqual(self.system.bookings[0]["status"], "Cancelled")

    def test_cancel_unknown_id(self):
        with self.assertRaises(ValueError):
            self.system.cancel("B9999")
        self.assertEqual(self.system.bookings[0]["status"], "Confirmed")

    def test_cancelled_id_is_never_reused(self):
        self.system.cancel("B1001")
        new_booking = self.system.book("Sara", 22, "R101", 1)
        self.assertEqual(new_booking["booking_id"], "B1002")


class TestReports(unittest.TestCase):
    def setUp(self):
        self.system = ReservationSystem()

    def test_empty_report_is_all_zero(self):
        self.assertEqual(self.system.report(), {
            "total_bookings": 0, "confirmed_bookings": 0, "cancelled_bookings": 0,
            "seats_reserved": 0, "revenue": 0, "fully_booked_routes": 0,
        })

    def test_report_excludes_cancelled_revenue(self):
        self.system.book("A", 30, "R101", 2)   # 2400
        self.system.book("B", 30, "R103", 3)   # 2400
        self.system.book("C", 30, "R105", 30)  # 45000, makes R105 full
        self.system.cancel("B1001")
        report = self.system.report()
        self.assertEqual(report["total_bookings"], 3)
        self.assertEqual(report["confirmed_bookings"], 2)
        self.assertEqual(report["cancelled_bookings"], 1)
        self.assertEqual(report["seats_reserved"], 33)
        self.assertEqual(report["revenue"], 47400)
        self.assertEqual(report["fully_booked_routes"], 1)

    def test_report_by_route(self):
        self.system.book("A", 30, "R101", 2)
        self.system.book("B", 30, "R101", 1)
        self.system.cancel("B1002")
        rows = {row["route_id"]: row for row in self.system.report_by_route()}
        self.assertEqual(rows["R101"], {"route_id": "R101", "seats": 2, "revenue": 2400})
        self.assertEqual(rows["R102"]["seats"], 0)

    def test_schedule_groups_by_departure_city(self):
        schedule = self.system.schedule()
        self.assertEqual([r["route_id"] for r in schedule["Karachi"]], ["R101", "R102", "R104"])
        self.assertEqual(schedule["Mirpur Khas"], [])
        self.assertEqual(schedule["Lahore"], [])

    def test_availability_status_labels(self):
        route = self.system.find_route("R101")
        self.assertEqual(self.system.availability_status(route), "Available")
        self.system.book("A", 30, "R101", 1)
        self.assertEqual(self.system.availability_status(route), "Partially Booked")


if __name__ == "__main__":
    unittest.main()
