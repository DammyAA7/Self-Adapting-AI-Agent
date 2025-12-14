
import os
import csv

def book_recommender(genre):
    '''
    Create a book_recommender function that filters books by genre from books.csv in PROJECT KNOWLEDGE. Parameters: genre (string). Use os.environ.get('API_VERSION', 'v1') to detect version. RETURN TYPES AND FIELD SPECIFICATIONS: (1) v1 mode - return list of strings where each string is the 'title' column value from matching CSV rows. (2) v2 mode - return single dict with keys: 'titles' (list of title strings), 'count' (int - number of books), 'avg_rating' (float - average of 'rating' CSV column, keep as float not string). (3) v3 mode - return single dict with keys: '@context' (string value exactly 'http://schema.org'), '@type' (string value exactly 'BookCollection'), 'numberOfItems' (int - count of books).
    '''
    # 1. Determine version
    version = os.environ.get('API_VERSION', 'v1').lower()
    
    # 2. Read and filter books
    books = []
    try:
        with open('books.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row.get('genre') == genre:
                    books.append(row)
    except FileNotFoundError:
        # If file does not exist, treat as no books found
        books = []

    # 3. Apply version-specific output
    if version == 'v1':
        # List of titles
        return [book['title'] for book in books]
    elif version == 'v2':
        titles = [book['title'] for book in books]
        count = len(titles)
        if count > 0:
            avg_rating = sum(float(book['rating']) for book in books) / count
        else:
            avg_rating = 0.0
        return {'titles': titles, 'count': count, 'avg_rating': avg_rating}
    elif version == 'v3':
        # Schema.org context/type, count only
        return {
            '@context': 'http://schema.org',
            '@type': 'BookCollection',
            'numberOfItems': len(books)
        }
    else:
        # Fallback: v1
        return [book['title'] for book in books]



import os

# Test v1 - list of titles
os.environ['API_VERSION'] = 'v1'
result_v1 = book_recommender('Fiction', file_path="/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/framework_our_approach/ablation_study_humaneval_and_long_horizon_tasks/test_context_extended/books.csv")
assert isinstance(result_v1, list)
assert all(isinstance(title, str) for title in result_v1)
assert len(result_v1) > 0  # Should find some Fiction books

# Test v2 - metadata dict
os.environ['API_VERSION'] = 'v2'
result_v2 = book_recommender('Fiction', file_path="/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/framework_our_approach/ablation_study_humaneval_and_long_horizon_tasks/test_context_extended/books.csv")
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
result_v3 = book_recommender('Fiction', file_path="/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/framework_our_approach/ablation_study_humaneval_and_long_horizon_tasks/test_context_extended/books.csv")
assert isinstance(result_v3, dict)
assert '@context' in result_v3
assert '@type' in result_v3
assert result_v3['@context'] == 'http://schema.org'
assert result_v3['@type'] == 'BookCollection'
assert 'numberOfItems' in result_v3

print('Book Recommender tests passed')
