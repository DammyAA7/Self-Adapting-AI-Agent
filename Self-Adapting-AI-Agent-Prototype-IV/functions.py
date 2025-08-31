# Dynamically generated functions will be added here



import re

def validate_email_addresses(emails):
    """Validates a list of email addresses and returns a dict mapping each unique address to its validity."""
    if not isinstance(emails, list):
        raise TypeError("emails must be provided as a list")
    pattern = re.compile(r'^[A-Za-z0-9._+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$')
    result = {}
    for email in emails:
        if not isinstance(email, str):
            raise TypeError("all items in the email list must be strings")
        if email in result:
            continue
        result[email] = bool(pattern.match(email))
    return result


if __name__ == "__main__":
    pass

if __name__ == "__main__":
    pass
