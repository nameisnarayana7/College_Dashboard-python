# 🎓 College Dashboard System

A desktop-based **College Dashboard System** built with **Python, Tkinter, SQLite, and Matplotlib**.

The application provides a simple interface for managing students, recording attendance, maintaining marks, exporting attendance data, and generating visual reports.

## 🚀 Features

### 👨‍💼 Admin Module

* Add new students
* Edit student details
* Delete students
* Search students by:

  * Roll Number
  * Name
  * Department
* View all registered students

### 📅 Attendance Module

* Mark daily attendance
* Mark students as **Present** or **Absent**
* View attendance records
* Refresh attendance data
* Export attendance records to CSV

### 📝 Marks Module

* Add marks for students
* Store subject-wise marks
* View student marks
* Calculate average marks for each student

### 📊 Reports Module

* Attendance summary chart
* Average marks chart
* Interactive Matplotlib charts inside the Tkinter application

### 💾 Database

The application uses **SQLite** for storing:

* Student information
* Attendance records
* Marks

The database file is automatically created as:

```text
college_dashboard.db
```

## 🛠️ Technologies Used

| Technology | Purpose                   |
| ---------- | ------------------------- |
| Python     | Core programming language |
| Tkinter    | Desktop GUI               |
| SQLite     | Database management       |
| Matplotlib | Data visualization        |
| CSV        | Attendance data export    |

## 📁 Project Structure

```text
College-Dashboard/
│
├── college_dashboard.py
├── college_dashboard.db
├── README.md
└── requirements.txt
```

> `college_dashboard.db` will be created automatically when the application runs, so it does not need to be included in the repository.

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/nameisnarayana7/College_Dashboard-python
```

### 2. Open the project

```bash
cd College-Dashboard
```

### 3. Install the required dependency

```bash
python -m pip install matplotlib
```

Or install from `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

## 📦 Requirements

Create a `requirements.txt` file containing:

```text
matplotlib
```

The following modules are part of Python's standard library and normally do not require pip installation:

```text
sqlite3
tkinter
datetime
csv
```

## ▶️ Run the Application

Run:

```bash
python college_dashboard.py
```

The College Dashboard window will open.

## 🧪 Sample Data

The application includes an option to import sample student data from:

```text
File → Import sample data
```

Sample students and marks are generated for demonstration purposes.

## 🖥️ Application Workflow

```text
                    College Dashboard
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
      Admin            Attendance           Marks
        │                  │                  │
   Manage Students    Mark Present/       Add Marks
   Search Students       Absent           View Marks
   Edit/Delete        Export CSV
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                       Reports
                           │
                  ┌────────┴────────┐
                  │                 │
             Attendance        Average Marks
                Chart              Chart
```

## 📊 Database Tables

### Students

```text
id
roll
name
dept
```

### Attendance

```text
id
student_id
date
status
```

### Marks

```text
id
student_id
subject
marks
```

## 🔐 Data Management

Student, attendance, and marks information is stored locally using SQLite. The application performs database operations such as:

* INSERT
* SELECT
* UPDATE
* DELETE

Student records are connected to attendance and marks through the student's database ID.

## 📈 Future Improvements

Possible improvements include:

* 🔐 Admin login and authentication
* 📱 Mobile/web version
* 📊 More advanced analytics
* 📅 Attendance percentage calculation
* 📄 PDF report generation
* 📧 Email reports
* 👨‍🎓 Student login
* 👨‍🏫 Faculty login
* ☁️ Cloud database integration
* 📤 Excel export
* 🎨 Improved modern UI

## 🎯 Learning Outcomes

This project demonstrates practical usage of:

* Python OOP
* GUI development with Tkinter
* SQLite database operations
* CRUD operations
* Data visualization
* CSV file handling
* Event-driven programming
* Basic application architecture

## 👨‍💻 Author

**Lakshmi Narayana Kondeti**

Computer Science Graduate | AI/ML & Python Developer

GitHub:
https://github.com/nameisnarayana7

Portfolio:
https://nameisnarayana7.github.io/portfolio_CV/

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.
