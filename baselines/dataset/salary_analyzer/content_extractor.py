"""
Content Extractor Class
Extracts content from web pages
"""
import re
from typing import List


class ContentExtractor:
    """Extracts content from web pages"""

    def __init__(self):
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.phone_pattern = r'\b\d{3}-\d{3}-\d{4}\b|\b\(\d{3}\)\s*\d{3}-\d{4}\b'
        self.url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+[^\s<>"{}|\\^`\[\].,;]'

    def extract_emails(self, text: str) -> List[str]:
        """Extract email addresses from text"""
        return re.findall(self.email_pattern, text)

    def extract_phone_numbers(self, text: str) -> List[str]:
        """Extract phone numbers from text"""
        return re.findall(self.phone_pattern, text)

    def extract_urls(self, text: str) -> List[str]:
        """Extract URLs from text content"""
        return re.findall(self.url_pattern, text)

    def extract_text_between_tags(self, html: str, tag: str) -> List[str]:
        """Extract text content between HTML tags"""
        pattern = f'<{tag}[^>]*>(.*?)</{tag}>'
        matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)
        return [match.strip() for match in matches]

    def clean_html_text(self, html: str) -> str:
        """Remove HTML tags and clean text"""
        # Remove HTML tags
        clean_text = re.sub(r'<[^>]+>', '', html)
        # Remove extra whitespace
        clean_text = ' '.join(clean_text.split())
        return clean_text
