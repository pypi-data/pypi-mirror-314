import json
import time
import uuid
from cryptography.fernet import Fernet
from eshare.utils import generate_key


def encrypt_file(file_path: str, password: str, output: str = None) -> str:
    """Encrypt a file with a password and store metadata in the encrypted file."""
    # Generate the key for encryption
    key = generate_key(password)
    cipher = Fernet(key)

    # Read the file data
    with open(file_path, "rb") as file:
        data = file.read()

    # Encrypt the data
    encrypted_data = cipher.encrypt(data)

    # Metadata to be embedded in the encrypted file
    token = str(uuid.uuid4())  # Generate a unique token for this file
    metadata = {
        "file_name": file_path,
        "key": key.decode(),  # Store key as a string
        "expiry": None,  # No expiry initially (optional, can be set later)
        "token": token,  # Save the token with the metadata
    }

    # Convert metadata to bytes and calculate the size
    metadata_json = json.dumps(metadata).encode("utf-8")
    metadata_size = len(metadata_json)

    # Combine metadata size + metadata + encrypted data
    file_data = metadata_size.to_bytes(4, "big") + metadata_json + encrypted_data

    # Determine the output file path
    encrypted_file = output or f"{file_path}.enc"

    # Write combined data to the encrypted file
    with open(encrypted_file, "wb") as file:
        file.write(file_data)

    return encrypted_file


def decrypt_file(file_path: str, password: str, output: str, stored_key: bytes) -> str:
    """Decrypt a file with a password and check if the file is valid."""
    key = generate_key(password)
    if key != stored_key:
        raise ValueError("Incorrect password.")

    # Open and read the encrypted file
    with open(file_path, "rb") as file:
        file_data = file.read()

    # Extract metadata size and metadata from the encrypted file
    metadata_size = int.from_bytes(file_data[:4], "big")
    metadata_json = file_data[4 : 4 + metadata_size]

    # Decode and load metadata
    metadata = json.loads(metadata_json.decode("utf-8"))
    file_name = metadata["file_name"]
    stored_key = metadata["key"].encode()  # The key from metadata
    expiry_time = metadata.get("expiry")

    # Check if the expiration time has passed (if metadata contains an expiry time)
    if expiry_time and time.time() > expiry_time:
        raise ValueError("File has expired.")

    # Extract encrypted data
    encrypted_data = file_data[4 + metadata_size :]

    # Decrypt the data
    cipher = Fernet(stored_key)
    decrypted_data = cipher.decrypt(encrypted_data)

    # Determine the output file path
    decrypted_file = output or file_name.replace(".enc", "")

    # Write the decrypted data to the output file
    with open(decrypted_file, "wb") as file:
        file.write(decrypted_data)

    return decrypted_file
