import os
import csv

def book_recommender(genre):
    csv_path = os.path.join('book_recommender', 'books.csv')
    version = os.environ.get('API_VERSION', 'v1')
    titles = []
    ratings = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['genre'] == genre:
                titles.append(row['title'])
                try:
                    ratings.append(float(row['rating']))
                except (ValueError, KeyError):
                    pass
    if version == 'v1':
        return titles
    elif version == 'v2':
        avg_rating = sum(ratings) / len(ratings) if ratings else 0.0
        return {
            'titles': titles,
            'count': len(titles),
            'avg_rating': avg_rating
        }
    elif version == 'v3':
        return {
            '@context': 'http://schema.org',
            '@type': 'BookCollection',
            'numberOfItems': len(titles)
        }
    else:
        # Default to v1 if unknown version
        return titles