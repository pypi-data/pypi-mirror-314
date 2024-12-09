import hashlib


def hash_email(email: str) -> str:
    """Hash an email address using SHA-256."""
    return hashlib.sha256(email.encode()).hexdigest()
