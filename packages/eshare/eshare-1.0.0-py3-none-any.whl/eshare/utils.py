import base64
import hashlib

SALT = b"eshare-app-salt"


def generate_key(password: str) -> bytes:
    """Generate a consistent encryption key from a password."""
    return base64.urlsafe_b64encode(
        hashlib.pbkdf2_hmac(
            "sha256",  # Hash algorithm
            password.encode(),  # Convert the password to bytes
            SALT,  # Static salt
            100000,  # Number of iterations
        )
    )
