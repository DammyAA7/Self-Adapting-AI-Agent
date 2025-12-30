# Add project root to path for imports
import sys
sys.path.insert(0, '/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent')

# Generated code by MetaGPT
import csv
import os
import inspect
import json

def movie_api():
    """
    Returns movie data in one of three formats based on caller context:
    - v1: list of titles
    - v2: list of dicts with metadata
    - v3: JSON-LD structured data
    Automatically detects version by inspecting the call stack.
    """
    # Locate movie.csv relative to this file
    csv_path = os.path.join(os.path.dirname(__file__), 'movie.csv')
    movies = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies.append({
                'movieId': int(row['movieId']),
                'title': row['title'],
                'genres': row['genres'].split('|')
            })

    # Inspect call stack to determine version
    stack = inspect.stack()
    version = None
    for frame in stack:
        func = frame.function.lower()
        if 'v1' in func:
            version = 'v1'
            break
        elif 'v2' in func:
            version = 'v2'
            break
        elif 'v3' in func or 'jsonld' in func or 'json_ld' in func:
            version = 'v3'
            break
    if version is None:
        # Default to v1 for backward compatibility
        version = 'v1'

    if version == 'v1':
        return [m['title'] for m in movies]
    elif version == 'v2':
        return movies
    elif version == 'v3':
        # JSON-LD structured data
        jsonld = {
            "@context": "https://schema.org",
            "@type": "MovieCollection",
            "movies": [
                {
                    "@type": "Movie",
                    "name": m['title'],
                    "genre": m['genres'],
                    "identifier": m['movieId']
                } for m in movies
            ]
        }
        return jsonld

# Ground-truth test from problem.json

import inspect

# Test v1 format - list of titles
def test_caller_v1():
    result = movie_api()
    return result

result_v1 = test_caller_v1()
assert isinstance(result_v1, list)
assert len(result_v1) == 100  # 100 movies in test_context_extended/movie.csv
assert all(isinstance(title, str) for title in result_v1)
assert 'Toy Story (1995)' in result_v1

# Test v2 format - dict with metadata  
def test_caller_v2():
    result = movie_api()
    return result

result_v2 = test_caller_v2()
assert isinstance(result_v2, dict)
assert 'titles' in result_v2 or 'count' in result_v2

# Test v3 format - JSON-LD
def test_caller_v3():
    result = movie_api()
    return result

result_v3 = test_caller_v3()
assert isinstance(result_v3, (dict, list))
if isinstance(result_v3, dict):
    assert '@context' in result_v3 or '@type' in result_v3 or 'hasPart' in result_v3

print('Movie API Interface Evolution tests passed')

