# School Management System

## Description
This project is for a basic idea of how a school management system looks like.
It's built using Django Rest Framework.

## Features

- Classes

      Add, Retrieve, Update, Delete and List Classes

- Sections

      Add, Retrieve, Update, Delete and List Sections
      Section have ForeignKey relationship with Classes 

- Subjects

      Add, Retrieve, Update, Delete and List Subjects

- Teachers

      Add, Retrieve, Update, Delete and List Teachers
      Teachers have ManyToMany relationship with Subjects and Sections of Classes

- Students

      Add, Retrieve, Update, Delete and List Classes
      Students have ManyToMany relationship with Subjects and ForeignKey relationship with Sections of Classes 

- Staff

      Add, Retrieve, Update, Delete and List Staff with thei ROLES

- Attendance (with Facial Recognition)

      ✨ Face-based attendance marking using facial recognition
      ✨ Automatic status determination (Present/Late) based on dynamic school timings
      ✨ Dynamic school timing configuration (Admin-only)
      ✨ Automatic marking of absentees at dismissal time using Celery
      - Face registration and verification
      - Daily attendance tracking with facial recognition
      - Monthly attendance reports and statistics
      - Configurable school timings (arrival, late threshold, dismissal)
      - Only ONE active timing at a time (enforced)
      - Automated absent marking via scheduled tasks
      
      📖 See SCHOOL_TIMING_API.md for school timing management
      📖 See ATTENDANCE_SETUP.md for detailed setup and usage instructions
      

- Results

      Add, Retrieve, Update, Delete and List Student Results
      Results have ForeignKey relationships with Student and Teacher  
      Result can only be generated if the user has is_teacher == True role
      Teacher's performance can also be identfied by calculating the average of the result of all the Sections Teacher teaches in

- Accounts

      Add, Retrieve, Update, Delete and List Students Payments
      Add, Retrieve, Update, Delete and List Teachers and Staff Salaries
      Add, Retrieve, Update, Delete and List Other Expenditures
