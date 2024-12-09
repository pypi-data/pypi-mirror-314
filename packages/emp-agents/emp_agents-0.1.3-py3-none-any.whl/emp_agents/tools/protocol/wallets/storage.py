import base64
import json
import os
from pathlib import Path

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def store_private_key(data: str, password: str, filename: str = "wallet.enc") -> None:
    """
    Store an Ethereum private key encrypted with a password.

    Args:
        private_key: The private key to encrypt and store
        password: Password to encrypt the private key
        filename: Name of file to store encrypted key (default: wallet.enc)
    """
    # Generate a salt
    salt = os.urandom(16)

    # Create key derivation function
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )

    # Generate key from password
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))

    # Create Fernet cipher
    fernet = Fernet(key)

    # Encrypt the private key
    encrypted_key = fernet.encrypt(data.encode())

    # Store encrypted key and salt
    encrypted_data = {
        "salt": base64.b64encode(salt).decode("utf-8"),
        "encrypted_key": encrypted_key.decode("utf-8"),
    }

    # Create storage directory if it doesn't exist
    storage_dir = Path.home() / ".wallets"
    storage_dir.mkdir(exist_ok=True)

    # Save to file
    with open(storage_dir / filename, "w") as f:
        json.dump(encrypted_data, f)


def load_private_key(password: str, filename: str = "wallet.enc") -> str:
    """
    Load and decrypt an Ethereum private key.

    Args:
        password: Password to decrypt the private key
        filename: Name of file containing encrypted key (default: wallet.enc)

    Returns:
        The decrypted private key
    """
    storage_path = Path.home() / ".wallets" / filename

    # Load encrypted data
    with open(storage_path) as f:
        data = json.load(f)

    salt = base64.b64decode(data["salt"])

    # Recreate key derivation function
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )

    # Regenerate key from password
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))

    # Decrypt
    fernet = Fernet(key)
    decrypted_key = fernet.decrypt(data["encrypted_key"].encode())

    return decrypted_key.decode()
