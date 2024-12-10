def safe_dn(dn: str) -> str:
    """
    Normalizes a Distinguished Name (DN) string.

    - Replaces OID representations (e.g., "1.2.840.113549.1.9.1") with readable names.
    - Splits the DN into key-value pairs, trims whitespace, converts to lowercase,
      and sorts the components for consistent representation.

    Args:
        dn (str): The DN string to normalize.

    Returns:
        str: A normalized DN string.

    Raises:
        ValueError: If the DN string is invalid or improperly formatted.
    """
    try:
        # Replace OID with human-readable names (e.g., emailAddress)
        dn = dn.replace("1.2.840.113549.1.9.1", "emailAddress")

        # Split the DN into components by commas
        components = dn.split(",")
        normalized_components = []
        for component in components:
            # Split each component into key-value pairs and normalize
            key, value = map(lambda part: part.strip().lower(), component.split("="))
            normalized_components.append(f"{key}={value}")

        # Sort components to ensure consistent order
        normalized_components.sort()

        # Join components back into a single DN string
        return ",".join(normalized_components)
    except Exception as error:
        # Log and raise errors for debugging or future diagnostics
        print("Error normalizing DN:", error)
        raise ValueError("Invalid DN format")


def parse_x509_certificate(cert_base64: str) -> dict:
    """
    Parses a Base64-encoded X.509 certificate in DER format and extracts key details.

    This function decodes a Base64 DER-encoded certificate, extracts key information
    such as serial number, subject DN, issuer DN, and validity periods, and normalizes
    DN strings for consistent formatting.

    Args:
        cert_base64 (str): Base64-encoded DER-formatted X.509 certificate.

    Returns:
        dict: A dictionary containing the following keys:
            - `x509`: The raw cryptography x509 object.
            - `serial`: The certificate serial number.
            - `subject_dn`: A dictionary with "raw" (original) and "normalized" DN values.
            - `issuer_dn`: A dictionary with "raw" (original) and "normalized" DN values.
            - `not_valid`: A dictionary with `before` and `after` validity period as datetime objects.

    Raises:
        ValueError: If decoding, parsing, or extraction fails.
    """

    import base64

    try:
        from cryptography import x509
        from cryptography.hazmat.backends import default_backend
    except ImportError as e:
        raise ImportError(f"Failed to import required modules: {e}")

    try:
        # Decode the base64-encoded certificate to DER format
        der_cert = base64.b64decode(cert_base64)
    except Exception as e:
        raise ValueError(f"Failed to decode base64 certificate: {e}")

    try:
        # Load the DER-formatted X.509 certificate
        x509_cert = x509.load_der_x509_certificate(der_cert, default_backend())
    except Exception as e:
        raise ValueError(f"Failed to parse DER X.509 certificate: {e}")

    try:
        # Extract certificate details
        serial_number = x509_cert.serial_number
        subject_dn = x509_cert.subject.rfc4514_string()
        issuer_dn = x509_cert.issuer.rfc4514_string()
        not_valid_before = x509_cert.not_valid_before_utc
        not_valid_after = x509_cert.not_valid_after_utc

        # Normalize the Distinguished Names
        subject_dn_normalized = safe_dn(subject_dn)
        issuer_dn_normalized = safe_dn(issuer_dn)

    except Exception as e:
        raise ValueError(f"Failed to extract certificate details: {e}")

    # Return extracted details as a structured dictionary
    return {
        "x509": x509_cert,
        "serial": serial_number,
        "subject_dn": {"raw": subject_dn, "normalized": subject_dn_normalized},
        "issuer_dn": {"raw": issuer_dn, "normalized": issuer_dn_normalized},
        "not_valid": {"before": not_valid_before, "after": not_valid_after},
    }
