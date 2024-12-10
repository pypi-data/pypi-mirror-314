# x509-utils

`x509-utils` is a Python library for parsing and normalizing X.509 certificates in Base64 DER format. It extracts key certificate details such as the serial number, subject DN, issuer DN, and validity periods while providing support for consistent DN normalization.

## Features

- Parse Base64-encoded X.509 certificates in DER format.
- Extract certificate details including:
  - Serial Number
  - Subject Distinguished Name (DN)
  - Issuer Distinguished Name (DN)
  - Validity Period (Not Before and Not After)
- Normalize Distinguished Names for consistent formatting.
- Lightweight and easy to integrate into cryptographic and PKI workflows.

## Installation

Install the library via pip:

```bash
pip install x509-utils
```

## Usage

Here's an example of how to use `x509-utils` to parse an X.509 certificate:

```python
from x509_utils import parse_x509_certificate

# Base64-encoded DER certificate
client_cert: str = """
<insert your Base64-encoded certificate here>
"""

# Parse the certificate
decoded_cert = parse_x509_certificate(client_cert)

# Access certificate details
print("Serial Number:", decoded_cert["serial"])
print("Subject DN (raw):", decoded_cert["subject_dn"]["raw"])
print("Subject DN (normalized):", decoded_cert["subject_dn"]["normalized"])
print("Issuer DN (raw):", decoded_cert["issuer_dn"]["raw"])
print("Issuer DN (normalized):", decoded_cert["issuer_dn"]["normalized"])
print("Validity Period (Not Before):", decoded_cert["not_valid"]["before"])
print("Validity Period (Not After):", decoded_cert["not_valid"]["after"])
```

## API Reference

### `parse_x509_certificate(cert_base64: str) -> dict`

Parses a Base64-encoded X.509 certificate in DER format.

#### Arguments
- `cert_base64` (str): Base64-encoded DER-formatted X.509 certificate.

#### Returns
A dictionary with the following keys:
- `serial`: The certificate serial number.
- `subject_dn`: A dictionary containing the raw and normalized subject DN.
- `issuer_dn`: A dictionary containing the raw and normalized issuer DN.
- `not_valid`: A dictionary with `before` and `after` datetime objects indicating the validity period.

#### Raises
- `ValueError`: If the certificate is invalid or parsing fails.

### `safe_dn(dn: str) -> str`

Normalizes a Distinguished Name (DN) string by sorting and formatting components consistently.

#### Arguments
- `dn` (str): The DN string to normalize.

#### Returns
- A normalized DN string.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests to help improve this library.


# Generating a self-signed certificate
```shell
# Generate a Private Key
openssl genrsa -out tmp/test.key 2048

# Generate a Certificate Signing Request (CSR)
openssl req -new -key tmp/test.key -out tmp/test.csr -subj "/C=US/ST=Virginia/L=McLean/O=Test Company/OU=Engineering/CN=example.com"

# Generate a Self-Signed Certificate
openssl x509 -req -days 365 -in tmp/test.csr -signkey tmp/test.key -out tmp/test.crt

# Convert the Certificate to DER Format
openssl x509 -in tmp/test.crt -outform DER -out tmp/test.der

# Base64 Encode the DER File
base64 tmp/test.der > tmp/test_cert.base64
```