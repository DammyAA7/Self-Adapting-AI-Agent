import sys
import os
# Add parent directory to Python path for imports to work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from Unit_Test.functions import *
from functions import *

def test_validate_email_normal_case():
    # Valid RFC-compliant email with valid TLDs
    assert validate_email("user@example.com") == True
    assert validate_email("john.doe@sub.domain.co.uk") == True
    assert validate_email("user+tag@domain.com") == True
    assert validate_email("user_name-123@domain.io") == True
    assert validate_email("u@d.io") == True
    assert validate_email("a@b.cd") == True  # Reinforced: minimal valid email is accepted

def test_validate_email_invalid_email_cases():
    # Invalid emails - missing @, missing domain, etc.
    assert validate_email("userexample.com") == False
    assert validate_email("user@.com") == False
    assert validate_email("user@com") == False
    assert validate_email("@example.com") == False
    assert validate_email("user@") == False
    assert validate_email("user@@example.com") == False
    assert validate_email("user@domain..com") == False
    assert validate_email("user@domain.c") == False  # TLD too short (RFC requires at least 2 chars)
    assert validate_email("user@-domain.com") == False  # Domain cannot start with hyphen
    assert validate_email(".user@example.com") == False  # Local part cannot start with dot
    assert validate_email("user.@example.com") == False  # Local part cannot end with dot
    assert validate_email("user..name@example.com") == False  # Double dot in local part

def test_validate_email_edge_cases():
    # Edge cases - maximal/minimal lengths, allowed characters
    assert validate_email("a@b.cd") == True  # Reinforced: minimal valid with valid TLD
    assert validate_email("a" * 64 + "@example.com") == True  # Max local part (64 chars)
    assert validate_email("user@subdomain." + "a" * 63) == False  # Invalid TLD (just long string)
    assert validate_email("user@ex" + "a"*250 + ".com") == False  # Domain too long

def test_validate_email_minimal_valid_email():
    # Explicit test for minimal valid email address per reinforced req
    assert validate_email("a@b.cd") == True
    assert validate_email("x@y.zq") == True
    assert validate_email("1@2.de") == True

def test_validate_email_invalid_tld_cases():
    # TLDs that are invalid due to length or characters or that are not real TLDs
    assert validate_email("user@example.c") == False  # Too short
    assert validate_email("user@example.123") == False  # All numeric TLD, invalid
    assert validate_email("user@example.toolongtld") == False  # Not a real TLD (should not exist)
    assert validate_email("user@example.abcdefghi") == False  # Excessively long TLD (>6 chars, and not real)
    assert validate_email("user@example." + "a"*64) == False  # TLD too long per RFC
    assert validate_email("user@example.-com") == False  # TLD cannot start with hyphen
    assert validate_email("user@example.com-") == False  # TLD cannot end with hyphen
    assert validate_email("user@example.co_m") == False  # TLD cannot have underscore
    # Additional: test with actual invalid/non-existent TLDs
    assert validate_email("user@example.zzz") == False  # .zzz does not exist
    assert validate_email("user@example.invalidtld") == False  # .invalidtld is not real
    assert validate_email("user@domain.local") == False  # .local is not a public TLD
    assert validate_email("user@domain.test") == False  # .test is reserved, not real
    assert validate_email("user@domain.example") == False  # .example is reserved, not real
    assert validate_email("user@domain.foo") == False  # .foo is reserved, not real

def test_validate_email_valid_real_tlds():
    # Confirm acceptance of known valid TLDs
    assert validate_email("user@example.com") == True
    assert validate_email("user@example.net") == True
    assert validate_email("user@example.org") == True
    assert validate_email("user@example.gov") == True
    assert validate_email("user@example.edu") == True
    assert validate_email("user@example.co.uk") == True
    assert validate_email("user@example.info") == True
    assert validate_email("user@example.biz") == True
    assert validate_email("user@example.io") == True
    assert validate_email("user@example.ai") == True
    # Minimal valid emails with valid TLDs
    assert validate_email("a@b.fr") == True
    assert validate_email("j@k.us") == True

def test_validate_email_missing_input():
    # None, empty, whitespace
    assert validate_email("") == False
    assert validate_email(None) == False
    assert validate_email("   ") == False

def test_validate_email_wrong_type_handling():
    # Wrong input types
    assert validate_email(12345) == False
    assert validate_email([]) == False
    assert validate_email({}) == False
    assert validate_email(object()) == False

def test_validate_email_unicode_handling():
    # Unicode in local part and domain
    assert validate_email("üser@example.com") == False  # Non-ASCII local part
    assert validate_email("user@exämple.com") == False  # Non-ASCII domain
    assert validate_email("用户@例子.公司") == False  # Fully internationalized (if not supported)
    assert validate_email("test@xn--bcher-kva.ch") in [True, False]  # Punycode, may be accepted if supported

def test_validate_email_integration_with_safe_functions():
    # Integration: Use validate_email in context with other safe functions (no actual integration logic, just sample)
    valid = validate_email("admin@sample.org")
    # For demonstration: could be used as a check prior to adding user, etc.
    assert isinstance(valid, bool)

def test_validate_email_duplicate_and_repeated_calls():
    # The result should always be consistent for the same input
    r1 = validate_email("repeat@test.com")
    r2 = validate_email("repeat@test.com")
    assert r1 == r2
    # Minimal valid email repeated
    r3 = validate_email("a@b.cd")
    r4 = validate_email("a@b.cd")
    assert r3 == r4

def test_validate_email_uppercase_tld():
    # TLDs with uppercase letters should be validated case-insensitively
    assert validate_email("user@example.COM") == True
    assert validate_email("user@example.NET") == True
    assert validate_email("user@example.Co.Uk") == True
    # Minimal valid email with uppercase TLD
    assert validate_email("a@b.CD") == True

def test_validate_email_trailing_dot():
    # Email with trailing dot in domain is not valid
    assert validate_email("user@example.com.") == False
    assert validate_email("a@b.cd.") == False  # Minimal valid with trailing dot should be invalid

def test_validate_email_reserved_but_not_real_tlds():
    # These TLDs are reserved, not real TLDs for email
    assert validate_email("user@domain.local") == False
    assert validate_email("user@domain.example") == False
    assert validate_email("user@domain.invalid") == False
    assert validate_email("user@domain.test") == False
    # Minimal valid form with reserved TLDs should be invalid
    assert validate_email("a@b.local") == False
    assert validate_email("z@y.test") == False

def test_validate_email_minimal_valid_email_additional():
    # Additional minimal valid emails with real TLDs
    assert validate_email("a@b.it") == True
    assert validate_email("m@n.be") == True
    assert validate_email("c@d.pl") == True
    assert validate_email("e@f.se") == True

if __name__ == "__main__":
    pytest.main([__file__])
