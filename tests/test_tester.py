import os
import sys
import unittest
from unittest.mock import patch, mock_open

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.main import import_students, export_students, add_student, update_student_file, check_attendance, manage_attendance_data

class TestStudentManagement(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data="John Doe\nJane Doe\n")
    def test_import_students(self, mock_file):
        file_path = "students.csv"
        students = import_students(file_path)
        mock_file.assert_called_once_with(file_path, mode='r', newline='')
        self.assertEqual(students, ["John Doe", "Jane Doe"])


    def test_add_student(self):
        students = ["John Doe"]
        add_student(students, "Jane Doe")
        self.assertIn("Jane Doe", students)

    @patch("src.main.export_students")
    def test_update_student_file(self, mock_export_students):
        file_path = "students.csv"
        students = ["John Doe", "Jane Doe"]
        update_student_file(file_path, students)
        mock_export_students.assert_called_once_with(file_path, students)

    @patch("builtins.input", side_effect=["y", "n"])
    def test_check_attendance(self, mock_input):
        students = ["John Doe", "Jane Doe"]
        attendance = check_attendance(students)
        self.assertEqual(attendance, {"John Doe": True, "Jane Doe": False})

    @patch("src.main.check_attendance", return_value={"John Doe": True, "Jane Doe": False})
    def test_manage_attendance_data(self, mock_check_attendance):
        students = ["John Doe", "Jane Doe"]
        attendance = manage_attendance_data(students)
        self.assertEqual(attendance, {"John Doe": True, "Jane Doe": False})
        mock_check_attendance.assert_called_once_with(students)

if __name__ == "__main__":
    unittest.main()

