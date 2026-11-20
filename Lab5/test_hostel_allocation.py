"""Regression tests for the hostel allocation lab."""

import unittest

import hostel_allocation as hostel


class HostelAllocationTests(unittest.TestCase):
    """Verify the main allocation, vacancy, and fee behaviors."""

    def setUp(self):
        hostel.load_config()

    def test_room_capacity_and_gender(self):
        self.assertEqual(hostel.allocate_room("S1", "Arjun", "M", 1), "A1")
        self.assertEqual(hostel.allocate_room("S2", "Kabir", "M", 2), "A1")
        self.assertEqual(hostel.allocate_room("S3", "Rohan", "M", 3), "A2")
        self.assertEqual(hostel.allocate_room("F1", "Diya", "F", 1), "B1")
        self.assertEqual(hostel.rooms["A1"]["occupants"], ["S1", "S2"])

    def test_duplicate_allocation_keeps_original_room(self):
        hostel.allocate_room("S1", "Arjun", "M", 1)
        hostel.allocate_room("S2", "Kabir", "M", 2)
        self.assertEqual(hostel.allocate_room("S1", "Arjun", "M", 1), "A1")
        self.assertEqual(hostel.rooms["A1"]["occupants"], ["S2", "S1"])

    def test_vacate_removes_occupant_and_updates_vacancies(self):
        hostel.allocate_room("S1", "Arjun", "M", 1)
        before = hostel.vacant_beds()
        self.assertTrue(hostel.vacate_room("S1"))
        self.assertNotIn("S1", hostel.rooms["A1"]["occupants"])
        self.assertEqual(hostel.vacant_beds(), before + 1)

    def test_seniority_and_vacant_beds(self):
        students = [{"year": 1}, {"year": 4}, {"year": 2}]
        ordered = [student["year"] for student in hostel.priority_order(students)]
        self.assertEqual(ordered, [4, 2, 1])
        self.assertEqual(hostel.vacant_beds(), 12)


if __name__ == "__main__":
    unittest.main()
