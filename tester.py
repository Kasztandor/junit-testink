import pytest
from unittest.mock import patch, mock_open
from main import import_students, export_students, add_student, update_student_file, check_attendance, manage_attendance_data

def test_import_students():
    with patch("builtins.open", new_callable=mock_open, read_data="John Doe\nJane Doe\n") as mock_file:
        file_path = "students.csv"
        students = import_students(file_path)
        mock_file.assert_called_once_with(file_path, mode='r', newline='')
        assert students == ["John Doe", "Jane Doe"]

def test_export_students():
    with patch("builtins.open", new_callable=mock_open) as mock_file:
        file_path = "students.csv"
        students = ["John Doe", "Jane Doe"]
        export_students(file_path, students)
        mock_file.assert_called_once_with(file_path, mode='w', newline='')
        mock_file().write.assert_has_calls([pytest.mock.call("John Doe\r\n"), pytest.mock.call("Jane Doe\r\n")])

def test_add_student():
    students = ["John Doe"]
    add_student(students, "Jane Doe")
    assert "Jane Doe" in students

def test_update_student_file():
    with patch("main.export_students") as mock_export_students:
        file_path = "students.csv"
        students = ["John Doe", "Jane Doe"]
        update_student_file(file_path, students)
        mock_export_students.assert_called_once_with(file_path, students)

def test_check_attendance():
    with patch("builtins.input", side_effect=["y", "n"]) as mock_input:
        students = ["John Doe", "Jane Doe"]
        attendance = check_attendance(students)
        assert attendance == {"John Doe": True, "Jane Doe": False}

def test_manage_attendance_data():
    with patch("main.check_attendance", return_value={"John Doe": True, "Jane Doe": False}) as mock_check_attendance:
        students = ["John Doe", "Jane Doe"]
        attendance = manage_attendance_data(students)
        assert attendance == {"John Doe": True, "Jane Doe": False}
        mock_check_attendance.assert_called_once_with(students)

