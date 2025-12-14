"""
Robots.txt Parser Class
Parses and respects robots.txt files
"""
from typing import List, Dict


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
