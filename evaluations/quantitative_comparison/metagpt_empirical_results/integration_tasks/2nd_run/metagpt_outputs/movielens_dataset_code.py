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