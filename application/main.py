import os
from datetime import date

import psycopg2
from psycopg2 import errors


def connect_db():
    """Connect to the PostgreSQL database"""
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "student_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.environ["DB_PASSWORD"],
    )


def getAllStudents():
    """Get and print the students"""
    with connect_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT student_id, first_name, last_name, email, enrollment_date FROM students ORDER BY student_id")
            rows = cursor.fetchall()
    if not rows:
        print("No students found.")
    for student_id, first_name, last_name, email, enrollment_date in rows:
        print(f"{student_id}: {first_name} {last_name} | {email} | {enrollment_date}")


def addStudent(first_name, last_name, email, enrollment_date):
    """Insert a student and print its ID"""
    with connect_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s) RETURNING student_id",
                (first_name, last_name, email, enrollment_date),
            )
            student_id = cursor.fetchone()[0]
    print(f"Student added with ID {student_id}.")


def updateStudentEmail(student_id, new_email):
    """Update a student email or print an error if the student can't be found"""
    with connect_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE students SET email = %s WHERE student_id = %s",
                (new_email, student_id),
            )
            updated = cursor.rowcount
    print("Email updated." if updated else "Student not found.")


def deleteStudent(student_id):
    """Delete a student or print an error if the student can't be found"""
    with connect_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
            deleted = cursor.rowcount
    print("Student deleted." if deleted else "Student not found.")


def main():
    """Show the menu and options"""
    while True:
        print("\n1. View students\n2. Add student\n3. Update student email\n4. Delete student\n5. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "5":
            print("Goodbye!")
            break
        try:
            if choice == "1":
                getAllStudents()
            elif choice == "2":
                first = input("First name: ").strip()
                last = input("Last name: ").strip()
                email = input("Email: ").strip()
                enrolled = input("Enrollment date (YYYY-MM-DD, blank for none): ").strip()
                if not first or not last or not email:
                    print("First name, last name and email are required.")
                    continue
                if enrolled:
                    enrolled = date.fromisoformat(enrolled)
                else:
                    enrolled = None
                addStudent(first, last, email, enrolled)
            elif choice == "3":
                student_id = int(input("Student ID: "))
                email = input("New email: ").strip()
                if not email:
                    print("Email cannot be blank.")
                    continue
                updateStudentEmail(student_id, email)
            elif choice == "4":
                student_id = int(input("Student ID: "))
                deleteStudent(student_id)
            else:
                print("Invalid option.")
        except (ValueError, psycopg2.Error) as exc:
            print(f"Operation failed: {exc}")


"""Catching errors"""
if __name__ == "__main__":
    try:
        main()
    except (KeyError, psycopg2.OperationalError) as exc:
        print(f"Database configuration or connection error: {exc}")
