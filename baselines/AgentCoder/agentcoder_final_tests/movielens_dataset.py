
import csv
import os
import json
import inspect

def movie_api():
    '''
    Create a movie_api function that automatically detects and switches between three different return formats based on the caller's context using movie.csv from PROJECT KNOWLEDGE: v1 returns list of titles, v2 returns dict with metadata, v3 returns JSON-LD structured data. The function must inspect the call stack to determine which version to use and maintain backward compatibility for all three simultaneously.
    '''
    # 1. Load the CSV data
    movies = []
    # Find the path to this script (assuming movie.csv is in the same directory)
    csv_path = os.path.join(os.path.dirname(__file__), 'movie.csv')
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Optionally convert movieId to int
            row['movieId'] = int(row['movieId'])
            movies.append(row)

    # 2. Inspect the call stack to determine required version
    stack = inspect.stack()
    # Look up the stack to find the caller (ignore first entry, which is ourselves)
    try:
        # Some safety: skip frames that are builtins or this same file, look for actual function
        for frame in stack[1:]:
            caller_name = frame.function.lower()  # function name
            # v3: jsonld
            if 'jsonld' in caller_name or 'ld' in caller_name:
                version = 3
                break
            # v2: dict or meta
            elif 'dict' in caller_name or 'meta' in caller_name:
                version = 2
                break
        else:
            version = 1  # default to v1
    finally:
        del stack  # Prevent reference cycles

    # 3. Output based on version
    if version == 1:
        # Return list of movie titles
        return [row['title'] for row in movies]
    elif version == 2:
        # Return list of dicts
        return movies
    elif version == 3:
        # Return JSON-LD structured data (as list of dict per movie)
        jsonld_items = []
        for row in movies:
            item = {
                "@context": {
                    "@vocab": "https://schema.org/",
                    "genres": "genre"
                },
                "@type": "Movie",
                "identifier": row['movieId'],
                "name": row['title'],
                "genre": row['genres'].split('|')
            }
            jsonld_items.append(item)
        return jsonld_items
    else:
        # Fallback: titles
        return [row['title'] for row in movies]



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
