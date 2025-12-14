"""
URL Validator Class
Validates and processes URLs
"""
import re
from typing import Optional
from urllib.parse import urljoin, urlparse


class URLValidator:
    """Validates and processes URLs"""

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if URL has valid format"""
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        return bool(re.match(pattern, url))

    @staticmethod
    def extract_domain(url: str) -> Optional[str]:
        """Extract domain from URL"""
        try:
            parsed = urlparse(url)
            return parsed.netloc
        except Exception:
            return None

    @staticmethod
    def normalize_url(url: str, base_url: str = None) -> str:
        """Normalize URL by joining with base if needed"""
        if base_url and not url.startswith(('http://', 'https://')):
            return urljoin(base_url, url)
        return url
