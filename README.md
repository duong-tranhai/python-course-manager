# Course Manager Backend (FastAPI)

This project is the backend system for a full-featured Course Manager application, built using FastAPI and PostgreSQL.

It supports student enrollment, lesson and quiz management, attendance tracking, progress monitoring, and role-based access control for students, teachers, and administrators.

# Requirements
Python 3.10 or higher
(Recommended: Python 3.10.x or 3.11.x for FastAPI and Pydantic v2 compatibility)

PostgreSQL 13 or higher

# INSTALLATION GUIDE
## Clone the repository:
```
git clone https://github.com/duong-tranhai/course-manager-backend.git

cd course-manager-backend
```

## Create and Activate a Virtual Environment:

### Windows
```
python -m venv venv

venv\Scripts\activate
```
### Mac/Linux
```
python3 -m venv venv

source venv/bin/activate
```

## Install dependencies:

```
pip install -r requirements.txt
```

## Configure environment variables:
Create a .env file for database URL, etc.
```
DATABASE_URL=postgresql://user:password@localhost:5432/course_manager_db
```
## Start the FastAPI server:
```
uvicorn app.main:app --reload
```

## 🚀 Features

### 👨‍🏫 Teacher

- **Course Management**: Create, edit, and delete courses.
- **Lesson Management**: Manage lessons inside courses.
- **Quiz Builder**: 
  - Add quizzes to lessons.
  - Multiple questions per quiz.
  - Set max attempts and passing scores.
- **Student Monitoring**:
  - View enrolled students.
  - Track lesson completion.
  - Quiz analytics.
- **Attendance Sessions**:
  - Create manual / auto / quiz-based sessions.
  - Mark student attendance manually.
- **Export Tools**:
  - Export attendance records as CSV.
  - View quiz performance metrics.

---

### 👨‍🎓 Student

- **Learning Dashboard**:
  - View enrolled courses with visual progress.
  - Navigate lessons and view quiz attempts.
- **Quizzes**:
  - Attempt quizzes with limited tries.
  - View score and correct answers after submission.
- **Attendance**:
  - Check in during active sessions.
  - Auto-marked absent if session ends without check-in.
- **Feedback**:
  - Submit course feedback after completion.

---

### 🛠️ Admin

- **User Management**:
  - View user list.
  - Assign/remove roles like Student, Teacher, Admin.
- **Role Management**:
  - Create, edit, delete user roles.
- **Course Oversight**:
  - View all courses.
  - Enrollment stats per course.
- **System Logs**:
  - Track user actions and system events.
  - Device info and IP captured. (Planned)
- **Login History** (Planned):
  - Monitor user login/logout activity.

---

## 🔐 Authentication

- JWT-based Auth with access & refresh tokens.
- Session timeout modal with 1-click session refresh.
- Role-based route protection for UI and API endpoints.

---

## ⚙️ Technical Stack

- **Backend**: FastAPI, SQLAlchemy, Alembic, PostgreSQL (or SQLite)
- **Frontend**: ReactJS, Axios, Bootstrap
- **Auth**: JWT with Refresh Token Strategy
- **Exports**: CSV downloads with Pandas
- **Background Tasks**: Mark absent after session timeout

🌟 Planned Features
- File upload for lessons

- Admin analytics dashboard (activity stats)

- PDF exports (for attendance or results)

- Enhanced feedback dashboard

- Notification & reminder system

- Certificate generation (after course completion)

👨‍💻 Author
- Developed by Duong Tran Hai with ❤️ using FastAPI + React.