# 👨‍💼 Employee Management System

A web-based **Employee Management System** developed to efficiently manage employee information through a simple and user-friendly interface.

The project uses **HTML, CSS, and JavaScript** for the frontend, **Python** for the backend, and **MySQL** for database management.

## 🚀 Features

* 🔐 User Login & Signup
* 📊 Interactive Dashboard
* ➕ Add New Employees
* ✏️ Update Employee Details
* 👁️ View Employee Information
* 🗑️ Delete Employee Records
* 🔎 Search Employee Details
* 💾 MySQL Database Integration
* 📱 User-friendly Interface
* 🔒 Basic User Authentication

## 🛠️ Technologies Used

### Frontend

* HTML5
* CSS3
* JavaScript

### Backend

* Python

### Database

* MySQL

### Development Tools

* Visual Studio Code
* MySQL Workbench
* Git & GitHub

## 📂 Project Structure

```text
Employee-Management-System/
│
├── frontend/
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── add_employee.html
│   ├── update_employee.html
│   └── view_employee.html
│
├── css/
│   └── style.css
│
├── js/
│   └── script.js
│
├── backend/
│   ├── server.py
│   └── database.py
│
├── database/
│   └── employee.sql
│
└── README.md
```

> The folder structure can be modified according to your actual project structure.

## ⚙️ Main Modules

### 🔐 Authentication

Users can create an account through the signup page and log in using their registered credentials.

### 📊 Dashboard

After successful login, users are redirected to the dashboard where employee information can be managed.

### ➕ Add Employee

Users can add new employee details such as:

* Employee ID
* Name
* Email
* Phone Number
* Position

### ✏️ Update Employee

Existing employee information can be modified whenever required.

### 👁️ View Employee

Users can view complete employee details stored in the system.

### 🗑️ Delete Employee

Employee records can be removed from the database when they are no longer required.

### 🗄️ MySQL Database

Employee information and user details are stored and managed using a MySQL database.

## 🔄 System Workflow

```text
Signup
   ↓
Login
   ↓
Dashboard
   ↓
Manage Employees
   ├── Add Employee
   ├── Update Employee
   ├── View Employee
   └── Delete Employee
   ↓
MySQL Database
```

## 💻 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Employee-Management-System.git
```

### 2. Open the Project

Open the project folder in **Visual Studio Code**.

### 3. Install Python

Make sure Python is installed on your system.

Check the version:

```bash
python --version
```

### 4. Setup MySQL

Open **MySQL Workbench** and create the required database.

Import or execute the SQL file:

```text
database/employee.sql
```

### 5. Configure Database

Update the MySQL connection details in the Python backend according to your system:

```python
host = "localhost"
user = "root"
password = "your_password"
database = "employee_db"
```

### 6. Run the Backend

```bash
python backend/server.py
```

### 7. Open the Application

Open the frontend in your browser or access it through the backend server, depending on your project configuration.

## 📸 Project Screenshots

Add your project screenshots here:

```text
screenshots/
├── login.png
├── signup.png
├── dashboard.png
├── add-employee.png
└── employee-details.png
```

## 🎯 Project Objective

The main objective of this project is to develop a simple and efficient system for managing employee records digitally. It reduces manual record management and provides an organized way to add, update, view, search, and delete employee information.

## 🔮 Future Enhancements

* Role-based authentication
* Employee attendance management
* Salary and payroll management
* Employee profile pictures
* Advanced search and filtering
* Export employee data to Excel/PDF
* Email notifications
* Responsive mobile interface

## 👨‍💻 Developer

**M.YuvaShankar**

B.Tech – Artificial Intelligence & Data Science

## 📄 License

This project is developed for educational and learning purposes.
