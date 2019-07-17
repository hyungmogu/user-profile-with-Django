# THPWD07 - User Profile with Django

This is the seventh project to team tree house's Python Web Tech Degree.

## Goal
- Build a form that takes in details about a registered user and displays those details on a profile page

## Deliverables / Objectives
1. Set up profile page
    - the page should be visible only once the user has logged in
    - the profile page includes 1) first name, 2) last name 3) date of birth 4) confirm email 5) short bio 6) option to upload avatar

2. Set up validation for email, date of birth and the biography.
    - Date of birth accepts three formats  YYYY-MM-DD, MM/DD/YYYY, or MM/DD/YY
    - Email validation checks if the email addresses match and is a valid format
    - Bio validation should check that the bio is 10 characters or longer and properly escapes HTML formatting

3. Set up "change password page" that updates user password
    - The page asks for 1) current password 2) new password 3) confirm password

4. Set up validation for "change password page" that
    - validates the current password, that the new password and confirm password fields match.
    - validates new password by making sure the following policies are satisfied
        - must not be the same as the current password
        - minimum password length of 14 characters.
        - must use of both uppercase and lowercase letters
        - must include of one or more numerical digits
        - must include of special characters, such as @, #, $
        - cannot contain the username or parts of the user’s full name, such as his first name


## Steps to Running/Exiting the Program
1. If not installed, install pipenv by typing `pip install pipenv` or `pip3 install pipenv` for python3 users
2. In project root folder, install dependencies by typing `pipenv install`
3. In project root folder, enter virtual environment by typing `pipenv shell`
4. In `profile_project` of project root folder, run `python manage.py makemigrations accounts`
4. In `profile_project` of project root folder, run `python manage.py migrate`
5. In `profile_project` of project root folder, run by typing `python manage.py runserver`
6. Open chrome and enter the url shown on console (i.e. `http://127.0.0.1:8000/`)
7. Once done, exit django by pressing `Ctrl`+`C` and virtual environment by typing `exit`