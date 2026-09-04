# Library Management System

A Django-based Library Management System that manages books, students, librarians, book requests, issuing, and returns.

## Features

- User authentication and logout
- Role-based access for Admin, Librarian, and Student
- Book and category management
- Book search and category filtering
- Student book requests
- Librarian request approval and rejection
- Book issuing with due dates
- Book return management
- Automatic book availability updates
- Student library history
- Admin dashboard with library statistics
- Responsive user interface

## User Roles

### Admin
- Manage users, books, categories, and library data through Django Admin
- View library statistics through the Admin Dashboard

### Librarian
- View pending book requests
- Approve or reject requests
- View issued books
- Process book returns

### Student
- Browse available books
- Search books by title
- Filter books by category
- Request books
- View request and issue history

## Technologies Used

- Python
- Django
- SQLite
- HTML
- CSS

## Project Structure

```text
library_management/
├── accounts/
├── books/
├── library/
├── library_management/
├── templates/
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md