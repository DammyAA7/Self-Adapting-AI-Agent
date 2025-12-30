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
    Reads movielens_dataset/movie.csv and returns movie data in one of three formats,
    automatically detecting the version based on the caller's context:
      - v1: list of titles
      - v2: list of dicts with metadata
      - v3: list of JSON-LD structured data

    The function inspects the call stack to determine which version to use.
    """
    # Determine the path to movie.csv relative to this file or cwd
    csv_path = os.path.join(os.path.dirname(__file__), "movie.csv") \
        if os.path.exists(os.path.join(os.path.dirname(__file__), "movie.csv")) \
        else os.path.join(os.getcwd(), "movielens_dataset", "movie.csv")

    # Read the CSV file
    movies = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            movies.append({
                "movieId": int(row["movieId"]),
                "title": row["title"],
                "genres": row["genres"].split('|') if row["genres"] else []
            })

    # Inspect the call stack to determine version
    stack = inspect.stack()
    version = None
    # Heuristic: look for 'v1', 'v2', or 'v3' in caller function/module/class names
    for frame in stack[1:]:
        name = frame.function.lower()
        module = frame.frame.f_globals.get("__name__", "").lower()
        code = frame.code_context[0].strip() if frame.code_context else ""
        if "v3" in name or "v3" in module or "v3" in code:
            version = "v3"
            break
        elif "v2" in name or "v2" in module or "v2" in code:
            version = "v2"
            break
        elif "v1" in name or "v1" in module or "v1" in code:
            version = "v1"
            break
    # Default to v1 for backward compatibility
    if version is None:
        version = "v1"

    if version == "v1":
        # Return list of titles
        return [movie["title"] for movie in movies]
    elif version == "v2":
        # Return list of dicts with metadata
        return movies
    elif version == "v3":
        # Return JSON-LD structured data
        jsonld = []
        for movie in movies:
            jsonld.append({
                "@context": "https://schema.org",
                "@type": "Movie",
                "name": movie["title"],
                "genre": movie["genres"],
                "identifier": movie["movieId"]
            })
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

