import os
import csv

def book_recommender(genre):
    """
    Filters books by genre from 'book_recommender/books.csv' and returns results
    based on API_VERSION environment variable.

    Args:
        genre (str): The genre to filter books by.

    Returns:
        Depending on API_VERSION:
            - v1: list of title strings.
            - v2: dict with keys 'titles', 'count', 'avg_rating'.
            - v3: dict with keys '@context', '@type', 'numberOfItems'.
    """
    csv_path = os.path.join('book_recommender', 'books.csv')
    matched_titles = []
    matched_ratings = []

    # Read and filter books by genre
    with open(csv_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['genre'] == genre:
                matched_titles.append(row['title'])
                try:
                    matched_ratings.append(float(row['rating']))
                except (ValueError, KeyError):
                    continue  # Skip rows with invalid or missing rating

    api_version = os.environ.get('API_VERSION', 'v1')

    if api_version == 'v1':
        return matched_titles
    elif api_version == 'v2':
        count = len(matched_titles)
        avg_rating = float(sum(matched_ratings) / count) if count > 0 else 0.0
        return {
            'titles': matched_titles,
            'count': count,
            'avg_rating': avg_rating
        }
    elif api_version == 'v3':
        return {
            '@context': 'http://schema.org',
            '@type': 'BookCollection',
            'numberOfItems': len(matched_titles)
        }
    else:
        # Default to v1 if unknown version
        return matched_titles