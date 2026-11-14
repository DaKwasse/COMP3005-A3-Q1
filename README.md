Student Database Assignment

Requirements
PostgreSQL and pgAdmin
Python
pip

1 Database setup

Start PostgreSQL and open pgAdmin

Create a database named student_db

Select student_db, open Query Tool and run database/setup.sql


How to run

Install the requirements:

python -m pip install -r requirements.txt

Set the database password:

(If running in windows Powershell)

$env:DB_PASSWORD = "YOUR_POSTGRES_PASSWORD"

Then run python application/main.py

Choose options 1–4 from the interactive menu to test these functions or 5 to exit

Application Functions

getAllStudents(): Displays all students in the database
addStudent(): Add a new student
updateStudentEmail(): Updates a student's email
deleteStudent(): Deletes a student

Verify changes in pgAdmin
After each operation run:

SELECT * FROM students ORDER BY student_id;


Demonstration video link: https://youtu.be/SUl9ru5BaTk
