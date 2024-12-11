# Eshare

`eshare` is a Python command-line tool for securely sharing files. It command-line tool for securely encrypting files, sharing them with time-limited tokens, and decrypting them using a password.

## Features

-   Encrypt files with a password.
-   Generate time-limited shareable tokens.
-   Decrypt files securely with the token and password.

## Installation

To install `eshare`, use pip:

```bash
pip install eshare
```

## Usage

Here’s a brief guide on how to use the `eshare` command-line tool.

### Encrypting a File

To encrypt a file, use the `eshare encrypt` command with the `--file` flag to specify the file and the `--password` flag for encryption.

```bash
eshare encrypt --file example.txt --password mypassword
```

This will encrypt `example.txt` using the provided password.

### Share a File

```bash
eshare share --file example.txt.enc --expire 24 --password mypassword
```

This will generate file shareable token, token is used to decrypt the file.

### Decrypting a File

To decrypt an encrypted file, use the `eshare decrypt` command along with the `--file`, `--token` and `--password` flags:

```bash
eshare decrypt --file example.txt.enc --token <token> --password mypassword
```

This will decrypt the encrypted file `example.txt.enc` using the provided token and password.

### Viewing Help

To view the help options and available commands for `eshare`, run:

```bash
eshare help
```

To view the help options for specific command, run:

```bash
eshare share --help
```

## Example

Here’s a complete example of encrypting and decrypting a file:

```bash
# Encrypt a file
eshare encrypt --file example.txt --password mypassword

# Share a file
eshare share --file example.txt.enc --expire 24 --password mypassword

# Decrypt the file
eshare decrypt --file example.txt.enc --token <token> --password mypassword
```

## About the Author

`eshare` is created by Parth Dudhatra (imParth), a passionate software engineer, developer advocate, and content creator known for his contributions to the tech community. He is passionate about Python programming, open-source software, and sharing knowledge with others.

Parth is active on various social media platforms, where he shares insights, tutorials, and tips related to programming, software development, and security. Connect with Parth Dudhatra on social media:

- [Portfolio](https://imparth.me)
- [X/Twitter](https://x.com/imparth73)
- [Instagram](https://instagram.com/imparth.dev)
- [GitHub](https://github.com/imparth7)
- [LinkedIn](https://linkedin.com/in/imparth7)
- [Medium](https://imparth7.medium.com)
- [Dev.to](https://dev.to/imparth)

If you have any questions, feedback, or suggestions, feel free to reach out to me on any platform!

## License

This project is licensed under the ISC License.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on the [GitHub repository](https://github.com/imparth7/eshare).

## Issues

If you encounter any issues, please report them on the [issues page](https://github.com/imparth7/eshare/issues).