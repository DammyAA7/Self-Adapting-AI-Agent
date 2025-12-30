# Add project root to path for imports
import sys
sys.path.insert(0, '/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent')

# Generated code by MetaGPT
import csv
import os
import json
import inspect

def movie_api():
    """
    Reads 'movie.csv' from 'movielens_dataset' and returns data in one of three formats,
    automatically selected based on the caller's context (by inspecting the call stack):
    - v1: list of titles
    - v2: dict with metadata
    - v3: JSON-LD structured data
    Maintains backward compatibility for all three versions.
    """
    # Locate the CSV file relative to this file or current working directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, 'movie.csv')
    if not os.path.exists(csv_path):
        # Try relative to cwd
        csv_path = os.path.join(os.getcwd(), 'movielens_dataset', 'movie.csv')
    if not os.path.exists(csv_path):
        raise FileNotFoundError("movie.csv not found in movielens_dataset")

    # Read the CSV
    movies = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies.append({
                "movieId": int(row["movieId"]),
                "title": row["title"],
                "genres": row["genres"].split('|')
            })

    # Inspect the call stack to determine version
    stack = inspect.stack()
    version = "v1"  # default

    # Heuristic: look for function name or module in stack
    for frame in stack:
        fname = frame.function.lower()
        modname = frame.frame.f_globals.get("__name__", "").lower()
        # Example heuristics, can be customized:
        if "v2" in fname or "v2" in modname:
            version = "v2"
            break
        elif "v3" in fname or "v3" in modname or "jsonld" in fname or "jsonld" in modname:
            version = "v3"
            break
        elif "v1" in fname or "v1" in modname:
            version = "v1"
            break
    # Also allow explicit override via environment variable for testing
    version = os.environ.get("MOVIE_API_VERSION", version)

    if version == "v1":
        # Return list of titles
        return [movie["title"] for movie in movies]
    elif version == "v2":
        # Return dict with metadata
        return {
            "count": len(movies),
            "movies": movies
        }
    elif version == "v3":
        # Return JSON-LD structured data
        jsonld = {
            "@context": "https://schema.org",
            "@type": "MovieCollection",
            "numberOfItems": len(movies),
            "itemListElement": [
                {
                    "@type": "Movie",
                    "identifier": movie["movieId"],
                    "name": movie["title"],
                    "genre": movie["genres"]
                }
                for movie in movies
            ]
        }
        return jsonld
    else:
        # Fallback to v1
        return [movie["title"] for movie in movies]

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

