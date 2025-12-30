# Add project root to path for imports
import sys
sys.path.insert(0, '/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent')

# Generated code by MetaGPT
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

# Ground-truth test from problem.json

import os

# Test v1 - list of titles
os.environ['API_VERSION'] = 'v1'
result_v1 = book_recommender('Fiction', file_path="/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/dataset/book_recommender/books.csv")
assert isinstance(result_v1, list)
assert all(isinstance(title, str) for title in result_v1)
assert len(result_v1) > 0  # Should find some Fiction books

# Test v2 - metadata dict
os.environ['API_VERSION'] = 'v2'
result_v2 = book_recommender('Fiction', file_path="/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/dataset/book_recommender/books.csv")
assert isinstance(result_v2, dict)
assert 'titles' in result_v2
assert 'count' in result_v2
assert 'avg_rating' in result_v2
assert isinstance(result_v2['titles'], list)
assert isinstance(result_v2['count'], int)
assert result_v2['count'] == len(result_v2['titles'])
assert isinstance(result_v2['avg_rating'], float)
assert 3.0 <= result_v2['avg_rating'] <= 5.0

# Test v3 - JSON-LD
os.environ['API_VERSION'] = 'v3'
result_v3 = book_recommender('Fiction', file_path="/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/dataset/book_recommender/books.csv")
assert isinstance(result_v3, dict)
assert '@context' in result_v3
assert '@type' in result_v3
assert result_v3['@context'] == 'http://schema.org'
assert result_v3['@type'] == 'BookCollection'
assert 'numberOfItems' in result_v3

print('Book Recommender tests passed')

