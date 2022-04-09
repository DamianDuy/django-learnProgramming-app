# Team Project

The overall goal of this application is to provide users an easy way to monitor their progress in learning custom programming languages. The road map of learning the chosen programming language will divide the learning path into the most important sections. At the end of each section the user will take part in a short test to check if they obtained the required knowledge to proceed.

**The supported programming languages include:<br />**
- C++

More programming languages will be added later.

The user can also indicate, which sections were the most difficult or the most engaging. Based on the users' answers the statistics will be made.

This application is meant to be used by anyone who learns programming and needs an extra motivation or the progress tracking.
It can also be used by programming courses' creators to check what topics are most problematic for users.

**Technology stack:<br />**
- Django framework<br />
- Chart.js JavaScript library for data visualization (the library's capabilities will be researched)

**Detailed list of functionalities:<br />**
- The user must create an account to be able to solve tests and add opinions<br />
- The user solves tests to progress<br />
- The user can evaluate the difficulty of the given topic<br />
- The user can create groups and see the progress of other users in the group - TO DO<br />
- In each topic, the amount of students who passed it, will be visible - TO DO<br />
- The administrator adds tests and learning topics<br />

**Research topics:<br />**
- The capabilities of Chart.js JavaScript library
- The statistics connected with the evaluation of the learning topics by users

# Setup
## Installation
Installation of Django:

```
$ python -m pip install Django
$ python -m pip install django-markdownx
$ python -m pip install django-utils-six
```

## Running a project
To run this project, change directory to directory where manage.py file is and run a command:

```
$ python manage.py runserver
```

## Running tests
To run unit tests, change directory to directory where manage.py file is and run a command:

```
$ python manage.py test
```

Now that the server’s running, visit http://127.0.0.1:8000/ with your Web browser. 
