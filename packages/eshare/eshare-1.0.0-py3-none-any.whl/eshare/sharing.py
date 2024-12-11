import os
import json
import time
import uuid


def generate_shareable_link(file_path: str, expire_hours: int, password: str) -> str:
    """Generate a time-limited token for sharing a file."""
    # Generate a unique token
    token = str(uuid.uuid4())

    # Set expiry time if needed
    expiry_time = time.time() + expire_hours * 3600

    # Add token and expiry time to the metadata of the encrypted file
    try:
        with open(file_path, "rb") as file:
            file_data = file.read()

        # Extract metadata size and metadata from the encrypted file
        metadata_size = int.from_bytes(file_data[:4], "big")
        metadata_json = file_data[4 : 4 + metadata_size]
        metadata = json.loads(metadata_json.decode("utf-8"))

        # Add token and expiry to the metadata
        metadata["token"] = token
        metadata["expiry"] = expiry_time

        # Convert updated metadata to bytes
        metadata_json_updated = json.dumps(metadata).encode("utf-8")
        metadata_size_updated = len(metadata_json_updated)

        # Combine metadata size + metadata + encrypted data
        file_data = (
            metadata_size_updated.to_bytes(4, "big")
            + metadata_json_updated
            + file_data[4 + metadata_size :]
        )

        # Write updated encrypted file
        with open(file_path, "wb") as file:
            file.write(file_data)

    except Exception as e:
        print(f"Error generating shareable link: {e}")

    return token


def validate_access(token: str) -> (str, bytes):  # type: ignore
    """Validate a token and return the file path and encryption key if valid."""
    # Here, the token is still used as a shared identifier.
    # However, all metadata extraction is done directly from the encrypted file.

    try:
        # The encrypted file path would include the token, or it could be explicitly passed.
        encrypted_file_path = f"{token}.enc"

        # Check if the file exists
        if not os.path.exists(encrypted_file_path):
            return None, None

        # Open and read the encrypted file to extract metadata
        with open(encrypted_file_path, "rb") as file:
            file_data = file.read()

        # Extract metadata size (first 4 bytes)
        metadata_size = int.from_bytes(file_data[:4], "big")
        metadata_json = file_data[4 : 4 + metadata_size]

        # Decode the metadata
        metadata = json.loads(metadata_json.decode("utf-8"))
        file_name = metadata["file_name"]
        stored_key = metadata["key"].encode()  # The key from metadata

        # Check if the expiration time has passed
        expiry_time = metadata.get("expiry")
        if time.time() > expiry_time:
            return None, None

        return file_name, stored_key

    except Exception as e:
        print(f"Error validating access: {e}")
        return None, None
