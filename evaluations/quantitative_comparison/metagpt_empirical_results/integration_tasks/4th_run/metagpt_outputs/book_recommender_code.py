import os
import csv

def book_recommender(genre):
    """
    Filters books by genre from books.csv in the book_recommender/ directory.
    Returns results according to API_VERSION (v1, v2, v3).

    Args:
        genre (str): The genre to filter books by.

    Returns:
        Depending on API_VERSION:
            - v1: list of title strings.
            - v2: dict with keys 'titles', 'count', 'avg_rating'.
            - v3: dict with keys '@context', '@type', 'numberOfItems'.
    """
    # Determine the path to books.csv relative to this file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, 'books.csv')

    # Read and filter books by genre
    titles = []
    ratings = []

    with open(csv_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['genre'] == genre:
                titles.append(row['title'])
                try:
                    ratings.append(float(row['rating']))
                except (ValueError, KeyError):
                    continue  # Skip rows with invalid or missing rating

    api_version = os.environ.get('API_VERSION', 'v1').lower()

    if api_version == 'v1':
        return titles
    elif api_version == 'v2':
        count = len(titles)
        avg_rating = float(sum(ratings) / count) if count > 0 else 0.0
        return {
            'titles': titles,
            'count': count,
            'avg_rating': avg_rating
        }
    elif api_version == 'v3':
        return {
            '@context': 'http://schema.org',
            '@type': 'BookCollection',
            'numberOfItems': len(titles)
        }
    else:
        # Default to v1 if unknown version
        return titles