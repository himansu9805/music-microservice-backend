"""Module for handling password hashing and verification."""
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import os
import base64


class PasswordHandler:
    """
    A class to handle password hashing and verification using the Scrypt key
    derivation function.

    Attributes:
        salt (bytes): The salt used for hashing. If not provided, a
        random 16-byte salt is generated.
        backend: The cryptographic backend used by the Scrypt function.

    Methods:
        hash_password(password: str) -> str:
            Hashes the given password using Scrypt and returns the hashed
            password as a base64-encoded string.

        verify_password(password: str, hashed: str) -> bool:
            Verifies the given password against the provided hashed password.
            Returns True if the password is correct, False otherwise.
    """

    def __init__(self, salt: bytes = None):
        self.salt = salt or os.urandom(16)
        self.backend = default_backend()

    def hash_password(self, password: str) -> str:
        """
        Hashes a password using the Scrypt key derivation function.
        Args:
            password (str): The password to be hashed.
        Returns:
            str: The hashed password encoded in URL-safe base64 format.
        """

        kdf = Scrypt(
            salt=self.salt,
            length=32,
            n=2**14,
            r=8,
            p=1,
            backend=self.backend
        )
        key = kdf.derive(password.encode())
        return base64.urlsafe_b64encode(self.salt + key).decode('utf-8')

    def verify_password(self, password: str, hashed: str) -> bool:
        """
        Verify if the provided password matches the hashed password.
        Args:
            password (str): The plain text password to verify.
            hashed (str): The base64 encoded hashed password to compare
                        against.
        Returns:
            bool: True if the password matches the hashed password,
                False otherwise.
        """

        decoded = base64.urlsafe_b64decode(hashed.encode('utf-8'))
        salt = decoded[:16]
        key = decoded[16:]
        kdf = Scrypt(
            salt=salt,
            length=32,
            n=2**14,
            r=8,
            p=1,
            backend=self.backend
        )
        try:
            kdf.verify(password.encode(), key)
            return True
        except Exception:
            return False
