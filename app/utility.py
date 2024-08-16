import os
import hashlib
import random
import string

def random_password(length: int = 10) -> str:
    """Generates a random password

    Args:
        length (int, optional): Length of the password. Defaults to 10.

    Returns:
        str: The generated password
    """
    notallowed = '²³{[]}^`´'
    letters = string.digits + string.ascii_letters + string.punctuation
    
    for x in notallowed:
        letters = letters.replace(x, '')
    
    pw = ''.join(random.choice(letters) for i in range(length))
    return pw

def hash_password(password: str) -> str:
    """Hashes a password

    Args:
        password (str): The password to hash

    Returns:
        str: The hashed password
    """

    salt = os.urandom(16)  # Generiere einen 16-Byte-Salt
    hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)

    return salt + hash_obj


def verify_password(stored_password: str, provided_password: str) -> bool:
    """Compares a stored hash password with a provided password

    Using a 16-Byte-Salt, the stored password is split into the salt and the hash.

    Args:
        stored_password (str): password from Database
        provided_password (str): User given Password

    Returns:
        bool: True if the passwords match, False otherwise
    """
    salt = stored_password[:16] 
    stored_hash = stored_password[16:] 
    hash_obj = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt, 100000)
    return hash_obj == stored_hash
