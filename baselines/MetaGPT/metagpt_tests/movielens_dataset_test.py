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
    Reads movie.csv in the current directory and returns data in one of three formats depending on the caller's context:
    - v1: list of movie titles
    - v2: list of dicts with metadata (movieId, title, genres)
    - v3: list of JSON-LD structured data for each movie
    The version is determined by inspecting the call stack for 'v1', 'v2', or 'v3' in the caller's function name or docstring.
    """
    # Helper to read the CSV
    def read_movies():
        movies = []
        with open(os.path.join(os.path.dirname(__file__), 'movie.csv'), encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                movies.append({
                    'movieId': row['movieId'],
                    'title': row['title'],
                    'genres': row['genres']
                })
        return movies

    # Inspect the call stack to determine version
    stack = inspect.stack()
    version = None
    for frame in stack[1:]:
        # Check function name
        fname = frame.function.lower()
        if 'v1' in fname:
            version = 'v1'
            break
        elif 'v2' in fname:
            version = 'v2'
            break
        elif 'v3' in fname:
            version = 'v3'
            break
        # Check docstring
        doc = inspect.getdoc(frame[0])
        if doc:
            doc_lower = doc.lower()
            if 'v1' in doc_lower:
                version = 'v1'
                break
            elif 'v2' in doc_lower:
                version = 'v2'
                break
            elif 'v3' in doc_lower:
                version = 'v3'
                break
    if version is None:
        # Default to v1 for backward compatibility
        version = 'v1'

    movies = read_movies()

    if version == 'v1':
        return [m['title'] for m in movies]
    elif version == 'v2':
        return movies
    elif version == 'v3':
        # JSON-LD structured data
        jsonld_list = []
        for m in movies:
            jsonld = {
                "@context": "https://schema.org",
                "@type": "Movie",
                "identifier": m['movieId'],
                "name": m['title'],
                "genre": m['genres'].split('|') if m['genres'] else []
            }
            jsonld_list.append(jsonld)
        return jsonld_list
    else:
        # Fallback to v1
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

