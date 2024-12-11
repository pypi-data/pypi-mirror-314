import typer
import json
import time
from eshare.encryption import encrypt_file, decrypt_file
from eshare.sharing import generate_shareable_link

app = typer.Typer()


@app.command()
def encrypt(
    file: str = typer.Option(..., "--file", "-f", help="Path to the file to encrypt"),
    password: str = typer.Option(
        ..., "--password", "-p", help="Password for encryption"
    ),
    output: str = typer.Option(None, "--output", "-o", help="Output file path"),
):
    """Encrypt a file with a password."""
    output_path = encrypt_file(file, password, output)
    typer.echo(f"File encrypted and saved as {output_path}")


@app.command()
def share(
    file: str = typer.Option(..., "--file", "-f", help="Path to the encrypted file"),
    expire_hours: int = typer.Option(
        24, "--expire", "-e", help="Expiration time in hours"
    ),
    password: str = typer.Option(
        ..., "--password", "-p", help="Password used during encryption"
    ),
):
    """Share an encrypted file by generating a shareable token."""
    token = generate_shareable_link(file, expire_hours, password)
    typer.echo(f"Shareable token: {token}")


@app.command()
def decrypt(
    file: str = typer.Option(..., "--file", "-f", help="Path to the encrypted file"),
    token: str = typer.Option(..., "--token", "-t", help="Token for decryption"),
    password: str = typer.Option(
        ..., "--password", "-p", help="Password for decryption"
    ),
    output: str = typer.Option(None, "--output", "-o", help="Output file path"),
):
    """Decrypt a file using the provided token and password."""
    try:
        # Open the encrypted file and extract metadata
        with open(file, "rb") as file_obj:
            file_data = file_obj.read()

        # Extract metadata size from the start of the file
        metadata_size = int.from_bytes(file_data[:4], "big")
        metadata_json = file_data[4 : 4 + metadata_size]
        metadata = json.loads(metadata_json.decode("utf-8"))

        # Extract token from the metadata
        extracted_token = metadata.get("token")
        if extracted_token != token:
            typer.echo("Error: Invalid token.")
            return

        # Validate expiration if metadata contains expiry time
        expiry_time = metadata.get("expiry")
        if expiry_time and time.time() > expiry_time:
            typer.echo("Error: The file has expired.")
            return

        # Extract the encryption key and the encrypted file data
        stored_key = metadata["key"].encode()  # Encryption key from metadata
        encrypted_data = file_data[4 + metadata_size :]  # noqa: F841

        # Decrypt the data using the provided password
        output_path = decrypt_file(file, password, output, stored_key)
        typer.echo(f"File decrypted and saved as {output_path}")

    except Exception as e:
        typer.echo(f"Error: {e}")


@app.command()
def help():
    """Display help information about the Eshare app."""
    typer.echo("""
Eshare CLI Tool: Securely encrypt, share, and decrypt files.

Commands:
  encrypt   Encrypt a file with a password.
  share     Generate a shareable link for the encrypted file.
  decrypt   Decrypt an encrypted file using a token and password.

Usage:
  encrypt --file/-f <file> --password/-p <password>
  share --file/-f <file> --expire/-t <hours> --password/-p <password>
  decrypt --file/-f <file> --token/-t <token> --password/-p <password>
""")


if __name__ == "__main__":
    app()
