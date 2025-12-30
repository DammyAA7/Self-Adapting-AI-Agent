import os
import json

def friend_suggestions(user_id):
    # Load social graph data
    with open('friend_suggester/social_graph.json', 'r') as f:
        data = json.load(f)
    users = {u['user_id']: u for u in data['users']}
    if user_id not in users:
        return []
    user = users[user_id]
    user_friends = set(user['friends'])
    user_interests = set(user['interests'])
    user_activity = user['activity']['level']
    mode = os.environ.get('RECOMMENDATION_MODE', 'basic').lower()
    suggestions = []
    for candidate_id, candidate in users.items():
        if candidate_id == user_id or candidate_id in user_friends:
            continue
        candidate_friends = set(candidate['friends'])
        candidate_interests = set(candidate['interests'])
        candidate_activity = candidate['activity']['level']
        # Mutual friends
        mutual_friends = len(user_friends & candidate_friends)
        score = 0.0
        if mode == 'basic':
            score = float(mutual_friends)
        elif mode == 'enhanced':
            common_interests = len(user_interests & candidate_interests)
            score = mutual_friends * 2.0 + common_interests * 1.5
        elif mode == 'advanced':
            common_interests = len(user_interests & candidate_interests)
            score = mutual_friends * 2.0 + common_interests * 1.5
            if user_activity == candidate_activity:
                score += 1.0
        else:
            score = float(mutual_friends)  # fallback to basic
        if score > 0:
            suggestions.append({'user_id': candidate_id, 'score': score})
    # Sort and return top 5
    suggestions.sort(key=lambda x: x['score'], reverse=True)
    return suggestions[:5]