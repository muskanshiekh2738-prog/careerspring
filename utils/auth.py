
import bcrypt
import sqlite3
from database.db import get_connection


def hash_password(password):
    """Securely hash a password."""
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode("utf-8")


def verify_password(password, hashed_password):
    """Verify a password against its stored hash."""
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


def register_user(name, email, password):
    """Register a new student account."""

    name = name.strip()
    email = email.strip().lower()

    if not name or not email or not password:
        return False, "All fields are required."

    if len(password) < 8:
        return False, "Password must contain at least 8 characters."

    connection = get_connection()
    cursor = connection.cursor()

    try:
        hashed_password = hash_password(password)

        cursor.execute(
            """
            INSERT INTO users (name, email, password)
            VALUES (?, ?, ?)
            """,
            (name, email, hashed_password)
        )

        connection.commit()
        return True, "Registration successful!"

    except sqlite3.IntegrityError:
        return False, "An account with this email already exists."

    finally:
        connection.close()


def login_user(email, password):
    """Authenticate a student."""

    email = email.strip().lower()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    )

    user = cursor.fetchone()
    connection.close()

    if user and verify_password(password, user["password"]):
        return True, dict(user)

    return False, None
