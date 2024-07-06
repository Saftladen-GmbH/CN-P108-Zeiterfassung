# Database

# Tables

- Users
- Login
- Logoff
- Admins
- Classes

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