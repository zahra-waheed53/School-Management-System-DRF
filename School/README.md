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

- Attendance

      Add, Retrieve, Update, Delete and List Teacher Attendance
      Add, Retrieve, Update, Delete and List Student Attendance
      Add, Retrieve, Update, Delete and List Staff Attendance
      

- Results

      Add, Retrieve, Update, Delete and List Student Results
      Results have ForeignKey relationships with Student and Teacher  
      Result can only be generated if the user has is_teacher == True role
      Teacher's performance can also be identfied by calculating the average of the result of all the Sections Teacher teaches in

- Accounts

      Add, Retrieve, Update, Delete and List Students Payments
      Add, Retrieve, Update, Delete and List Teachers and Staff Salaries
      Add, Retrieve, Update, Delete and List Other Expenditures
