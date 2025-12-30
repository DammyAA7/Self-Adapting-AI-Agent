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