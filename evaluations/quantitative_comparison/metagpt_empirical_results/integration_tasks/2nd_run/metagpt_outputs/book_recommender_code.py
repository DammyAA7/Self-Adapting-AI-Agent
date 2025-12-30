import os
import csv

def book_recommender(genre):
    """
    Filters books by genre from 'book_recommender/books.csv' and returns results
    according to API_VERSION (v1, v2, v3).

    Args:
        genre (str): The genre to filter books by.

    Returns:
        Depending on API_VERSION:
            - v1: list of title strings.
            - v2: dict with keys 'titles' (list), 'count' (int), 'avg_rating' (float).
            - v3: dict with keys '@context', '@type', 'numberOfItems' (int).
    """
    csv_path = os.path.join('book_recommender', 'books.csv')
    titles = []
    ratings = []

    # Read and filter the CSV
    with open(csv_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['genre'] == genre:
                titles.append(row['title'])
                try:
                    ratings.append(float(row['rating']))
                except (ValueError, KeyError):
                    continue  # Skip rows with invalid rating

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