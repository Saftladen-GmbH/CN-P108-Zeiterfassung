from os import urandom
from flask import redirect, url_for
from datetime import datetime
from hashlib import pbkdf2_hmac
from random import choice
from string import ascii_letters, digits, punctuation


def calculate_time_history(data: list, limit: int = None) -> dict:
    """Caclulate a Time delta between multiple days of login and logouts

    Args:
        data (list of lists or list of dicts):

            ! IMPORTANT: The input data MUST be sorted by datatime

            List of Dictionaries with the keys 'Time' and 'type'
            ! 'type' has to be either of: login or logout
            ! 'time' has to be a datetime object
            ! Script is ignoring todays date

            OR

            List of a list with an databaseobject at firstplace and the type at the second
            ! 'type' has to be either of: login or logout
            ! the object should have an attribut 'time'
            ! 'time' has to be a datetime object
            ! Script is ignoring todays date

            List of Dicts:
            example 1:
            [{'time': datetime.strptime('2000-12-03 7:00', '%Y-%m-%d %H:%M'), 'type': 'login'},
            {'time': datetime.strptime('2000-12-03 16:00', '%Y-%m-%d %H:%M'), 'type': 'logoout'}]

            example 2:
            [{'time': datetime.strptime('2000-12-01 07:00', '%Y-%m-%d %H:%M'), 'type': 'login'},
            {'time': datetime.strptime('2000-12-01 09:00', '%Y-%m-%d %H:%M'), 'type': 'logout'},
            {'time': datetime.strptime('2000-12-01 11:00', '%Y-%m-%d %H:%M'), 'type': 'login'},
            {'time': datetime.strptime('2000-12-01 16:00', '%Y-%m-%d %H:%M'), 'type': 'logout'},
            {'time': datetime.strptime('2000-12-02 07:00', '%Y-%m-%d %H:%M'), 'type': 'login'},
            {'time': datetime.strptime('2000-12-02 10:00', '%Y-%m-%d %H:%M'), 'type': 'logout'},
            {'time': datetime.strptime('2000-12-02 11:00', '%Y-%m-%d %H:%M'), 'type': 'login'},
            {'time': datetime.strptime('2000-12-02 16:00', '%Y-%m-%d %H:%M'), 'type': 'logout'},
            {'time': datetime.strptime('2000-12-03 7:00', '%Y-%m-%d %H:%M'), 'type': 'login'},
            {'time': datetime.strptime('2000-12-03 16:00', '%Y-%m-%d %H:%M'), 'type': 'logout'}]

            List of Lists:
            example 1:
            [[databaseobject, 'login'],
            [databaseobject, 'logout']]

        limit (int): the limit of days that get processed. Defaults to 'None'

    Raises:
        ValueError: Raise error if the type key is not correct

    Returns:
        dict: Return a dict with the keys beeing the date and the value beeing the timedelta object
    """
    work_hours = {}
    start = None
    end = None
    current_date = None
    for d in data:
        tmp = 0

        # ? Type checking
        if type(d) is dict:
            d_type = d["type"]
            d_time = d["time"]
        elif type(d) is list:
            d_type = d[1]
            d_time = d[0].Time
        else:
            raise SyntaxError("Given Data is not supported!")

        if limit is not None and len(work_hours) >= limit:
            print("Limit reached")
            break

        # ? Skip data if date is today
        if d_time.date() == datetime.now().date():
            continue

        # ? Reset values if new day is detected
        # if d_time.date() != current_date:
        #    start = None
        #    end = None

        current_date = d_time.date()

        # ? For Debug
        print("Calculating date: ", current_date)

        if d_type == "login":
            start = d_time
        elif d_type == "logout":
            end = d_time
        else:
            raise ValueError(f'Expected: "login" or "logout". Got: {d_type}')

        if start is not None and end is not None:
            tmp = end - start
            start = None
            end = None
            if str(current_date) not in work_hours:
                work_hours[str(current_date)] = tmp
            else:
                work_hours[str(current_date)] += tmp
    return work_hours


def verify_login(session, userid: str) -> bool:
    """Verifies if the user is logged in

    Args:
        session: The session object
        userid (str): The user ID

    Returns:
        bool: True if the user is logged in, False otherwise
    """
    return session.get("userid") == userid


def user_logout(session):
    """Logs out the user

    Args:
        session: The session object
    """
    print("Session before Pop: ", session.get("userid"))  # Debug
    session.pop("userid", None)
    print("Session after Pop: ", session.get("userid"))  # Debug
    return redirect(url_for("index"))


def image2blob(image_path: str) -> bytes:
    """Converts an image to a BLOB

    Args:
        image_path (str): Path to the image

    Returns:
        bytes: The image as a BLOB
    """
    with open(image_path, "rb") as file:
        return file.read()


def blob2image(blob: bytes, image_path: str) -> None:
    """Converts a BLOB to an image

    Args:
        blob (bytes): The BLOB to convert
        image_path (str): Path to save the image
    """
    with open(image_path, "wb") as file:
        file.write(blob)


def random_password(length: int = 10) -> str:
    """Generates a random password

    Args:
        length (int, optional): Length of the password. Defaults to 10.

    Returns:
        str: The generated password
    """
    notallowed = "²³{[]}^`´"
    letters = digits + ascii_letters + punctuation

    for x in notallowed:
        letters = letters.replace(x, "")

    pw = "".join(choice(letters) for i in range(length))
    return pw


def hash_password(password: str) -> str:
    """Hashes a password

    Args:
        password (str): The password to hash

    Returns:
        str: The hashed password
    """

    salt = urandom(16)  # Generiere einen 16-Byte-Salt
    hash_obj = pbkdf2_hmac("sha256", password.encode(), salt, 100000)

    return salt + hash_obj


def verify_password(stored_password: str, provided_password: str) -> bool:
    """Compares a stored hash password with a provided password

    Using a 16-Byte-Salt, the stored password is split into the
    salt and the hash.

    Args:
        stored_password (str): password from Database
        provided_password (str): User given Password

    Returns:
        bool: True if the passwords match, False otherwise
    """
    salt = stored_password[:16]
    stored_hash = stored_password[16:]
    hash_obj = pbkdf2_hmac("sha256", provided_password.encode(), salt, 100000)
    return hash_obj == stored_hash
