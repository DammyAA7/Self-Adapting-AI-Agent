# Add project root to path for imports
import sys
sys.path.insert(0, '/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent')

# Generated code by MetaGPT
import csv
import inspect
import json
import os

def movie_api():
    """
    Reads 'movie.csv' in the current directory and returns movie data in one of three formats based on caller context:
    - v1: list of movie titles
    - v2: list of dicts with metadata (movieId, title, genres)
    - v3: list of JSON-LD structured data for each movie
    The version is determined by inspecting the call stack for 'v1', 'v2', or 'v3' in the caller's function name, module, or filename.
    """
    # Helper to detect version from call stack
    def detect_version():
        stack = inspect.stack()
        for frame in stack:
            for key in ('function', 'filename', 'module'):
                val = getattr(frame, key, None) or frame[3] if key == 'function' else frame[1]
                if isinstance(val, str):
                    if 'v3' in val.lower():
                        return 'v3'
                    if 'v2' in val.lower():
                        return 'v2'
                    if 'v1' in val.lower():
                        return 'v1'
        # Default to v1 for backward compatibility
        return 'v1'

    version = detect_version()
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'movie.csv') if '__file__' in globals() else 'movie.csv'
    if not os.path.exists(csv_path):
        csv_path = 'movie.csv'  # fallback to current dir
    movies = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            movies.append({
                'movieId': row['movieId'],
                'title': row['title'],
                'genres': row['genres']
            })

    if version == 'v1':
        return [m['title'] for m in movies]
    elif version == 'v2':
        return movies
    elif version == 'v3':
        # JSON-LD format for each movie
        jsonld_movies = []
        for m in movies:
            jsonld = {
                "@context": "https://schema.org",
                "@type": "Movie",
                "name": m['title'],
                "genre": m['genres'].split('|'),
                "identifier": m['movieId']
            }
            jsonld_movies.append(jsonld)
        return jsonld_movies
    else:
        # fallback
        return [m['title'] for m in movies]

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

