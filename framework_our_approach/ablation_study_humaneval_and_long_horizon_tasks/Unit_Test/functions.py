from enum import Enum

class Status(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
import os
import csv

def book_recommender(genre, file_path):
    """Recommend books by genre based on API_VERSION (v1, v2, v3)."""
    api_version = os.getenv("API_VERSION", "v1").lower()
    # Load data from CSV
    with open(file_path, newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    # Filter by genre
    matched = [row for row in rows if row.get("genre") == genre]
    titles = [row.get("title") for row in matched]
    # Version-specific output
    if api_version == "v1":
        return titles
    if api_version == "v2":
        count = len(titles)
        if count:
            total = 0.0
            for row in matched:
                try:
                    total += float(row.get("rating", 0))
                except Exception:
                    total += 0.0
            avg_rating = total / count
        else:
            avg_rating = 0.0
        return {"titles": titles, "count": count, "avg_rating": avg_rating}
    if api_version == "v3":
        return {
            "@context": "http://schema.org",
            "@type": "BookCollection",
            "numberOfItems": len(titles)
        }
    # Fallback to v1 behavior
    return titles
