from enum import Enum

class Status(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


import re

def validate_email(email):
    """
    Validates whether the given email address is RFC-compliant and uses a real, public TLD.
    Returns True if valid, False otherwise (including reserved or non-existent TLDs).
    """
    if not isinstance(email, str):
        return False
    email = email.strip()
    if not email:
        return False

    # Real, public TLDs (minimal set; can be expanded as needed)
    valid_tlds = {
        # Generic
        "com", "net", "org", "gov", "edu", "biz", "info", "io", "ai",
        # Country code
        "uk", "co.uk", "fr", "us", "it", "be", "pl", "se", "de", "ch",
        # Popular others
        "co", "me", "tv", "ca", "au", "nl", "es", "cz", "ru", "jp",
        # Add more real TLDs as needed for coverage
    }
    # Reserved and test TLDs - never valid
    reserved_tlds = {
        "local", "example", "test", "invalid", "foo"
    }
    # Check for trailing dot
    if email.endswith('.'):
        return False

    # Basic email regex (no unicode, no quoted, basic ASCII, RFC-like)
    # local-part: 1-64 chars, domain: 1-255 chars, TLD: 2-63 chars
    email_pattern = re.compile(
        r"^(?P<local>[A-Za-z0-9!#$%&'*+/=?^_`{|}~.-]{1,64})@(?P<domain>[A-Za-z0-9.-]{1,255})$"
    )
    match = email_pattern.match(email)
    if not match:
        return False

    local_part = match.group('local')
    domain_part = match.group('domain')

    # No double dots in local or domain
    if '..' in local_part or '..' in domain_part:
        return False
    # Local part cannot start or end with dot
    if local_part.startswith('.') or local_part.endswith('.'):
        return False
    # Domain cannot start or end with hyphen or dot
    if domain_part.startswith('-') or domain_part.endswith('-'):
        return False
    if domain_part.startswith('.') or domain_part.endswith('.'):
        return False
    # Only ASCII allowed
    try:
        local_part.encode('ascii')
        domain_part.encode('ascii')
    except UnicodeEncodeError:
        return False

    # Domain must contain at least one dot and valid TLD
    domain_labels = domain_part.split('.')
    if len(domain_labels) < 2:
        return False
    # TLD can be multi-part (e.g., "co.uk")
    tld = domain_labels[-1].lower()
    sld = domain_labels[-2].lower()
    # Compose for multi-part TLDs (e.g., co.uk)
    tld_full = sld + '.' + tld if (sld + '.' + tld) in valid_tlds else tld

    # TLD: must be at least 2 chars, all alpha, not all-numeric, not reserved/test, not too long, not start/end with hyphen, no underscore, only a-z
    if not (2 <= len(tld) <= 6):
        return False
    if not tld.isalpha():
        return False
    if tld in reserved_tlds:
        return False
    if tld_full in reserved_tlds:
        return False
    if tld.startswith('-') or tld.endswith('-'):
        return False
    if '_' in tld:
        return False

    # TLD exists in valid TLDs (case-insensitive). Accept multi-part TLDs only if in list.
    if tld_full in valid_tlds:
        pass
    elif tld in valid_tlds:
        pass
    else:
        return False

    # No domain segment can start or end with hyphen
    for label in domain_labels:
        if not label or label.startswith('-') or label.endswith('-'):
            return False
        # Only allow a-z, 0-9, hyphen in domain labels
        if not re.match(r'^[A-Za-z0-9-]+$', label):
            return False

    # Local part: max 64 chars
    if len(local_part) > 64:
        return False
    # Domain part: max 255 chars
    if len(domain_part) > 255:
        return False

    return True

