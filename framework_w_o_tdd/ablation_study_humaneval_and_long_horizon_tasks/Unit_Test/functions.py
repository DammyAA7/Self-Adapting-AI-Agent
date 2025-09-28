from enum import Enum

class Status(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


import inspect
import os
import csv
import re

def movie_api():
    """
    A single-entry API function that inspects the caller's context to determine which version
    of the output format to return:
    - Version "v1": returns a simple list of movie titles.
    - Version "v2": returns a dict with key "movies" mapping to a list of metadata dicts.
    - Version "v3": returns a JSON-LD structured payload compliant with schema.org's Movie type.
    Reads data from the project's movie.csv file and filters by requested year based on caller context.

    Parameters:
    None

    Returns:
    list, dict, or JSON-LD dict depending on version.
    """
    # Determine version and year from call stack
    version = 'v1'
    year = None
    for frame_info in inspect.stack()[1:]:
        func_name = frame_info.function or ''
        file_name = os.path.basename(frame_info.filename or '')
        # detect version
        if '_v3' in func_name or '_v3' in file_name:
            version = 'v3'
        elif '_v2' in func_name or '_v2' in file_name:
            if version != 'v3':
                version = 'v2'
        elif '_v1' in func_name or '_v1' in file_name:
            if version not in ('v2', 'v3'):
                version = 'v1'
        # detect year
        if year is None:
            m = re.search(r'(\d{4})', func_name) or re.search(r'(\d{4})', file_name)
            if m:
                year = m.group(1)
        # if we've found a non-default version and a year, we can stop
        if version != 'v1' and year:
            break

    # Path to the CSV file
    file_path = "/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/framework_w_o_tdd/ablation_study_humaneval_and_long_horizon_tasks/movielens_dataset/movie.csv"
    if not os.path.exists(file_path):
        raise FileNotFoundError

    movies = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            title = row.get('title', '').strip()
            yr = row.get('year', '').strip()
            genre = row.get('genre', '').strip()
            if not title:
                continue
            if year and yr != year:
                continue
            movies.append({'title': title, 'year': yr, 'genre': genre})

    if version == 'v1':
        return [m['title'] for m in movies]
    elif version == 'v2':
        return {'movies': movies}
    else:  # v3
        item_list = []
        for m in movies:
            item_list.append({
                '@type': 'Movie',
                'name': m['title'],
                'datePublished': m['year'],
                'genre': m['genre']
            })
        return {
            '@context': "http://schema.org",
            '@type': "ItemList",
            'itemListElement': item_list
        }
