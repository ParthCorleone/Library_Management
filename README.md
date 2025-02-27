# Library Management System

## Project Overview
This is a **Library Management System** built using **Django** and **SQLite**. The system includes role-based access for different users such as **Admin, Librarian, Staff, and Customers**. Each role has specific functionalities to manage books, users, and reports.

## Live Demo
You can access the live project here: [Library Management System](https://parthdhinge.pythonanywhere.com/)

## Features
- **Admin:**
  - View reports on book issues and user activities
  - Manage books, staff, and librarians
  - Add and delete users
- **Librarian:**
  - Issue and return books
  - Manage book records
- **Staff:**
  - Assist in book management
- **Customer:**
  - Search and borrow books
  - View issued books and return them

## Tech Stack
- **Backend:** Django (Python)
- **Database:** SQLite
- **Frontend:** HTML5 (No CSS used)
- **Deployment:** PythonAnywhere

## Installation Guide
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/library-management-system.git
   cd library-management-system
   ```
2. Create a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```sh
   python manage.py migrate
   ```
5. Run the development server:
   ```sh
   python manage.py runserver
   ```

## Usage
- **Superuser Credentials:**
  To access the admin panel, create a superuser:
  ```sh
  python manage.py createsuperuser
  ```
  Then login at `http://127.0.0.1:8000/admin/`.

## Contributing
Contributions are welcome! Feel free to fork the repository and submit pull requests.

## License
This project is licensed under the MIT License.

## Author
Developed by [Parth Dhinge](https://github.com/yourusername)

