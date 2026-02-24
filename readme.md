![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Django](https://img.shields.io/badge/Django-5.1.5-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

# Attendance Management System

A web-based attendance management system built with Django that allows faculty members to track student attendance and provides students with access to their attendance records and analytics.

## Problem Statement

Managing attendance manually in educational institutions is time-consuming and error-prone. This system provides a centralized platform for tracking attendance, generating analytics, and improving transparency between faculty and students.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Design Decisions](#design-decisions)
- [Installation](#installation)
- [Usage](#usage)
- [Database Models](#database-models)
- [API Endpoints](#api-endpoints)
- [Screenshots](#screenshots)

## Features

### For Faculty
- **Dashboard**: View all assigned courses with student counts
- **Take Attendance**: Create sessions and mark attendance for students
- **View Attendance**: See detailed attendance records per course with student-wise breakdown
- **Reports**: Generate attendance reports with monthly trends, performance distribution, and student rankings

### For Students
- **Dashboard**: Overview of enrolled courses with attendance percentages
- **View Attendance**: Detailed attendance breakdown per course
- **Reports**: Visual analytics including:
  - Daily attendance trends
  - Course-wise attendance comparison
  - Overall attendance statistics

### General
- Role-based authentication (Student/Faculty)
- Responsive web interface
- Real-time attendance percentage calculations

## Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Django 5.1.5 |
| **Database** | SQLite |
| **Frontend** | HTML, CSS, Django Templates |
| **Authentication** | Django Auth (Custom User Model) |

## Project Structure

```
attendance-management/
├── Project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── authenticate/
│   ├── models.py              # User models (MyUser, Student, Faculty)
│   ├── views.py               # Login/logout views
│   ├── urls.py
│   ├── admin.py
│   ├── templates/
│   │   └── authenticate/
│   │       ├── home.html
│   │       ├── base_login.html
│   │       ├── faculty_login_page.html
│   │       └── student_login_page.html
│   └── static/
│       ├── css/
│       └── images/
├── attendance/
│   ├── models.py              # Course, Session, Attendance models
│   ├── views.py               # Dashboard, attendance, reports views
│   ├── urls.py
│   ├── admin.py
│   ├── templates/
│   │   └── attendance/
│   │       ├── base_faculty_dashboard.html
│   │       ├── base_student_dashboard.html
│   │       ├── faculty_dashboard.html
│   │       ├── student_dashboard.html
│   │       ├── take_attendance.html
│   │       ├── faculty_view_attendance.html
│   │       ├── student_view_attendance.html
│   │       ├── faculty_reports.html
│   │       └── student_reports.html
│   └── static/
│       └── css/
├── db.sqlite3
├── manage.py
├── add users.py               # Script to add users
└── add faculty.py             # Script to add faculty
```

## Design Decisions

- **UUID for session IDs**: `Session.session_id` uses `UUIDField` with `uuid.uuid4` to prevent predictable session enumeration and URL guessing
- **Custom user model**: `MyUser` extends `AbstractUser` via `AUTH_USER_MODEL`, making it easy to add fields later without schema migrations against the built-in `User` table
- **Role-based access control via `user_type`**: A single `user_type` field (`student`/`faculty`) on `MyUser` drives all access branching, keeping permission logic simple and centralised
- **Separate `authenticate` and `attendance` apps**: Authentication concerns (login, user profiles) are decoupled from attendance domain logic, making each app independently testable and replaceable
- **Profile models as OneToOne extensions**: `Student` and `Faculty` are thin proxy models linked to `MyUser` via `OneToOneField`, allowing domain-specific relationships (e.g. `CourseBatch.students`) without polluting the core user model
- **`unique_together` on Attendance**: `(session, student)` is enforced at the database level, preventing duplicate attendance records for the same session without extra application-layer checks
- **SQLite for development simplicity**: No external database setup required; the engine can be swapped to PostgreSQL in `settings.py` for production without changing any application code

## Installation

### Prerequisites
- Python 3.10+
- pip

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd attendance-management
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
     ```bash
     pip install -r requirements.txt
     ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (Admin)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Home: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

## Usage

### Adding Users

Use the provided scripts or Django admin:

```bash
python "add users.py"    # Add student users
python "add faculty.py"  # Add faculty users
```

Or via Django Admin:
1. Go to http://127.0.0.1:8000/admin/
2. Add users with appropriate `user_type` (student/faculty)
3. Create corresponding Student/Faculty profiles

### Workflow

1. **Admin Setup**:
   - Create Courses
   - Create CourseBatch (assign faculty and students)

2. **Faculty**:
   - Login at `/faculty_login/`
   - View dashboard with assigned courses
   - Take attendance for sessions
   - View attendance records and reports

3. **Student**:
   - Login at `/student_login/`
   - View dashboard with enrolled courses
   - Check attendance records
   - View attendance reports and analytics

## Database Models

### Authentication App

#### MyUser (Custom User)
| Field | Type | Description |
|-------|------|-------------|
| username | CharField | Unique identifier (roll no/faculty id) |
| name | CharField | Full name |
| email | EmailField | Email address |
| user_type | CharField | 'student' or 'faculty' |
| department | CharField | Department code |
| joined | DateField | Join date |

#### Student
- OneToOne relationship with MyUser

#### Faculty
- OneToOne relationship with MyUser

### Attendance App

#### Course
| Field | Type | Description |
|-------|------|-------------|
| name | CharField | Course name |
| code | CharField | Unique course code |
| department | CharField | Department |
| description | TextField | Course description |

#### CourseBatch
| Field | Type | Description |
|-------|------|-------------|
| course | ForeignKey | Reference to Course |
| faculty | ManyToMany | Assigned faculty |
| students | ManyToMany | Enrolled students |
| term | CharField | Batch and term info |
| start_date | DateField | Start date |
| end_date | DateField | End date |

#### Session
| Field | Type | Description |
|-------|------|-------------|
| session_id | UUIDField | Unique session ID |
| course_batch | ForeignKey | Reference to CourseBatch |
| date | DateField | Session date |
| topic | CharField | Session topic |

#### Attendance
| Field | Type | Description |
|-------|------|-------------|
| session | ForeignKey | Reference to Session |
| student | ForeignKey | Reference to Student |
| status | CharField | 'present' or 'absent' |
| timestamp | DateTimeField | Record timestamp |

## API Endpoints

| URL | View | Description |
|-----|------|-------------|
| `/` | home | Landing page |
| `/student_login/` | student_login_page | Student login |
| `/faculty_login/` | faculty_login_page | Faculty login |
| `/logout/` | logout_user | Logout |
| `/student_dashboard/` | student_dashboard | Student dashboard |
| `/faculty_dashboard/` | faculty_dashboard | Faculty dashboard |
| `/take_attendance/` | take_attendance | Mark attendance |
| `/take_attendance/<session_id>/` | take_attendance | Mark attendance for session |
| `/student_view_attendance/` | student_view_attendance | Student attendance view |
| `/faculty_view_attendance/` | faculty_view_attendance | Faculty attendance view |
| `/faculty_view_attendance/<course_id>/` | faculty_view_attendance | Course-specific attendance |
| `/student_reports/` | student_reports | Student analytics |
| `/faculty_reports/` | faculty_reports | Faculty analytics |

## Screenshots

### Home Page
Landing page with options for Student and Faculty login.

### Faculty Dashboard
Overview of assigned courses with student counts and quick actions.

### Take Attendance
Select course, create session, and mark attendance for enrolled students.

### Student Dashboard
Overview of enrolled courses with attendance percentages and statistics.

### Reports
Visual charts showing attendance trends, course comparisons, and performance metrics.

## License

MIT License
