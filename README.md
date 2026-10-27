# Employee Management System

**Course:** PC15 – Python Programming 2 with Lab  
**Institution:** National Teachers College  
**Activity:** Week 12 Midterm Examination – Milestone 2

## Description

The Employee Management System integrates a Tkinter desktop interface with Django's Object-Relational Mapper (ORM). It allows users to add, view, refresh, and delete employee records. Django Admin provides another interface for managing the same records.

## Technologies

- Python
- Tkinter
- Django
- SQLite

## Employee Fields

- `name` — employee name
- `position` — employee's job position
- `date_hired` — automatically recorded date and time

## Installation and Execution

1. Create and activate a Python virtual environment.
2. Install Django using `pip install -r requirements.txt`.
3. Run `python manage.py makemigrations employees`.
4. Run `python manage.py migrate`.
5. Create an administrator using `python manage.py createsuperuser`.
6. Start the web application using `python manage.py runserver`.
7. Open `http://127.0.0.1:8000/admin/` to manage employee records.
8. In a second terminal, run `python tkinter_app.py` to launch the desktop application.

## Validation

The application rejects blank employee names and positions and prevents inputs longer than 100 characters.

## Expected Result

The Tkinter application and Django Admin display records from the same SQLite database. The system supports employee record creation, viewing, and deletion.
