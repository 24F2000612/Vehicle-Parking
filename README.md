Vehicle Parking Management System
Introduction
This project is a web-based Vehicle Parking Management System built using Python and Flask.
It allows users to register, log in, search for parking locations, book and release parking spots, and view their parking history.
Admins can manage parking lots, oversee all bookings and users, and view analytics charts.
The goal is to make parking management simple, efficient, and accessible for both users and administrators.

Technologies Used
Python 3 — Main programming language

Flask — Web framework for handling routes and server logic

Flask-SQLAlchemy — ORM for database management

SQLite — Lightweight database for storing users, lots, spots, and reservations

Jinja2 — Templating engine for dynamic HTML pages

Bootstrap — For responsive and clean user interface

Matplotlib — To generate charts and analytics on the server side

Features
User Registration & Login —  sign-up and authentication for users and admins

Parking Lot Management — Admins can add, edit, and remove parking locations and spots

Spot Booking & Release — Users can search for available parking, book a spot, and release it after use

Search Functionality — Search parking by location or address

Booking History — Users can view their recent parking activity and costs

Admin Dashboard — Overview of all users, parking lots, bookings, and system statistics

Summary Charts — Visual analytics for bookings and parking usage

Role-Based Access — Separate dashboards and permissions for users and admins

Project Structure
text
/models           # Database models
/templates        # HTML templates (Jinja2)
/static           # Static files (CSS, images)
app.py            # Main Flask application
README.md         # Project documentation
How to Run
Clone this repository

git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
Install dependencies

pip install flask flask_sqlalchemy matplotlib
Start the app

python app.py
Open your browser and go to http://127.0.0.1:5000/

Why this project?
Parking management is a common real-world problem.
This project demonstrates how web development, database design, and user authentication can be combined to solve such problems efficiently.
