"""
Web Crawling and URL Processing Module
Handles web scraping, URL validation, and content extraction
"""
import re
from typing import List, Dict, Set, Optional, Tuple
from urllib.parse import urljoin, urlparse
import time


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


class CrawlManager:
    """Manages web crawling operations with rate limiting"""
    
    def __init__(self, delay_seconds: float = 1.0, max_retries: int = 3):
        self.delay_seconds = delay_seconds
        self.max_retries = max_retries
        self.visited_urls: Set[str] = set()
        self.failed_urls: Set[str] = set()
        self.crawl_stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'total_time': 0.0
        }
    
    def add_visited_url(self, url: str) -> None:
        """Mark URL as visited"""
        self.visited_urls.add(url)
    
    def is_url_visited(self, url: str) -> bool:
        """Check if URL has been visited"""
        return url in self.visited_urls
    
    def add_failed_url(self, url: str) -> None:
        """Mark URL as failed"""
        self.failed_urls.add(url)
    
    def should_skip_url(self, url: str) -> bool:
        """Determine if URL should be skipped"""
        return url in self.visited_urls or url in self.failed_urls
    
    def apply_rate_limit(self) -> None:
        """Apply rate limiting delay"""
        time.sleep(self.delay_seconds)
    
    def update_stats(self, success: bool, request_time: float) -> None:
        """Update crawling statistics"""
        self.crawl_stats['total_requests'] += 1
        self.crawl_stats['total_time'] += request_time
        
        if success:
            self.crawl_stats['successful_requests'] += 1
        else:
            self.crawl_stats['failed_requests'] += 1
    
    def get_success_rate(self) -> float:
        """Calculate success rate as percentage"""
        total = self.crawl_stats['total_requests']
        if total == 0:
            return 0.0
        return (self.crawl_stats['successful_requests'] / total) * 100
    
    def get_average_request_time(self) -> float:
        """Calculate average request time"""
        total = self.crawl_stats['total_requests']
        if total == 0:
            return 0.0
        return self.crawl_stats['total_time'] / total


class RobotsTxtParser:
    """Parses and respects robots.txt files"""
    
    def __init__(self, robots_content: str = ""):
        self.rules: Dict[str, List[str]] = {}
        self.crawl_delay: Dict[str, float] = {}
        self.parse_robots_txt(robots_content)
    
    def parse_robots_txt(self, content: str) -> None:
        """Parse robots.txt content"""
        current_user_agent = None
        
        for line in content.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if line.lower().startswith('user-agent:'):
                current_user_agent = line.split(':', 1)[1].strip()
                if current_user_agent not in self.rules:
                    self.rules[current_user_agent] = []
            
            elif line.lower().startswith('disallow:'):
                if current_user_agent:
                    path = line.split(':', 1)[1].strip()
                    self.rules[current_user_agent].append(path)
            
            elif line.lower().startswith('crawl-delay:'):
                if current_user_agent:
                    try:
                        delay = float(line.split(':', 1)[1].strip())
                        self.crawl_delay[current_user_agent] = delay
                    except ValueError:
                        continue
    
    def can_fetch(self, user_agent: str, url_path: str) -> bool:
        """Check if user agent can fetch the given URL path"""
        # Check specific user agent rules first
        if user_agent in self.rules:
            for disallowed_path in self.rules[user_agent]:
                if url_path.startswith(disallowed_path):
                    return False
        
        # Check wildcard rules
        if '*' in self.rules:
            for disallowed_path in self.rules['*']:
                if url_path.startswith(disallowed_path):
                    return False
        
        return True
    
    def get_crawl_delay(self, user_agent: str) -> float:
        """Get crawl delay for user agent"""
        return self.crawl_delay.get(user_agent, self.crawl_delay.get('*', 0.0))


# Example usage patterns
if __name__ == "__main__":
    # URL processing
    validator = URLValidator()
    sample_url = "https://example.com/page"
    is_valid = validator.is_valid_url(sample_url)
    domain = validator.extract_domain(sample_url)
    
    # Content extraction
    extractor = ContentExtractor()
    sample_text = "Contact us at info@example.com or call (555) 123-4567"
    emails = extractor.extract_emails(sample_text)
    phones = extractor.extract_phone_numbers(sample_text)
    
    # Crawl management
    crawler = CrawlManager(delay_seconds=2.0)
    crawler.add_visited_url(sample_url)
    success_rate = crawler.get_success_rate()
    
    # Robots.txt handling
    robots_content = "User-agent: *\\nDisallow: /private/\\nCrawl-delay: 1"
    robots = RobotsTxtParser(robots_content)
    can_crawl = robots.can_fetch("*", "/public/page")