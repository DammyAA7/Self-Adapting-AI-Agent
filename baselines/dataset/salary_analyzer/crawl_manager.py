"""
Crawl Manager Class
Manages web crawling operations with rate limiting
"""
import time
from typing import Set, Dict


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
