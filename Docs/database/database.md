# Database

## Tables

- Users
- Login
- Logoff
- Admins
- Classes

### Purpose

This Database is used to primarily track user login and logoff times. Those times will be display in a webapp and should be managed by a specific admin, who can add and delete users. He should also be able to determine the classes if a new user is added.

### Datasecurity

For now Userdata is stored unencrypted in the Database.

Passwords are hashed and then stored, but not encrypted.

Later, the Userdata should be encrypted with an EE2E solution.

## Table Contents

### Users

- UID (Primary)
- Name
- Firstname
- DOB [Date of Birth]
- CA (Foreign)

### Login

- NR (Primary - Autoincrement)
- Time
- UID (Foreign)

### Logoff

- NR (Primary - Autoincrement)
- Time
- UID (Foreign)

### Admins

- Username (Primary)
- Password
- UID (Foreign)

### Classes

- CA (Primary)[Class abbreviation]
- Subject_area
- Classroom