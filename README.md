# University Management System

A web-based University Management System built with Flask, SQLAlchemy, and Flask-Migrate. This project allows you to manage various entities such as students, staff, courses, faculties, and degree programs. The system comes with sample data for testing and a modern, responsive UI using Tailwind CSS and DataTables.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Database Setup](#database-setup)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Overview

University Management System is designed to help administrators manage university-related data efficiently. The application supports adding and listing students, staff, courses, faculties, and degree programs. It also includes automated sample data creation for quick testing and development.

## Features

- **Student Management:** Add, view, and manage student records (including admission status, course enrollment, and degree assignment).
- **Staff Management:** Add and manage staff members with unique staff IDs.
- **Course Management:** Add and manage courses with details such as course code, capacity, and enrollment count.
- **Faculty Management:** Manage faculties and assign existing staff members, courses, and degree programs.
- **Degree Program Management:** Add degree programs along with admission requirements.
- **Sample Data Generation:** Automatically generate sample data for a fully functional demo.
- **Responsive UI:** Modern design using Tailwind CSS and enhanced tables using DataTables for a smooth user experience.

## Installation

### Prerequisites

- Python 3.7 or higher
- [Git](https://git-scm.com/)
- Virtual Environment Manager (e.g., `venv` or Conda)

### Steps

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Nkalipho/university-management-system.git
    cd university-management-system
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database and migrations:**

    Initialize the database using Flask-Migrate:
    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

## Usage

1. **Run the application:**

    ```bash
    python app.py
    ```

2. **Open your browser:**

    Navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000) to view the application.

3. **Navigation:**

    Use the navigation links (e.g., "Add Student", "Add Staff", "Add Course", "Faculties", etc.) to manage the various entities.

## Database Setup

This project uses SQLite as its database, with SQLAlchemy as the ORM and Flask-Migrate to handle database migrations.

- **Migrations:**
  
  If you modify any of the models in `models.py`, create a new migration:
  ```bash
  flask db migrate -m "Describe your changes"
  flask db upgrade
  ```

## Project Structure

```
 university-management-system/
 ├── app.py             # Main application entry point
 ├── models.py          # Database models
 ├── routes.py          # Application routes
 ├── templates/         # HTML templates
 ├── static/            # Static files (CSS, JS)
 ├── migrations/        # Database migrations
 ├── requirements.txt   # Python dependencies
 ├── README.md          # Project documentation
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m "Add new feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgements

Special thanks to all contributors and open-source libraries that made this project possible.

