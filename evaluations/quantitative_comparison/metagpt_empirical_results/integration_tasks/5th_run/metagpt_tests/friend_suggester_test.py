# Add project root to path for imports
import sys
sys.path.insert(0, '/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent')

# Generated code by MetaGPT
import os
import json

def friend_suggestions(user_id):
    """
    Recommend friends for a given user_id using the data in friend_suggester/social_graph.json.
    Supports three modes based on the RECOMMENDATION_MODE environment variable:
      - 'basic': score = number of mutual friends
      - 'enhanced': score = mutual friends * 2.0 + common interests * 1.5
      - 'advanced': as enhanced, plus 1.0 bonus if activity levels match
    Returns a list of up to 5 dicts, each with 'user_id' and 'score', sorted by score descending.
    """
    # Load social graph data
    data_path = os.path.join(os.path.dirname(__file__), 'social_graph.json')
    with open(data_path, 'r', encoding='utf-8') as f:
        social_graph = json.load(f)

    users = social_graph.get('users', [])
    user_map = {user['user_id']: user for user in users}

    if user_id not in user_map:
        return []

    # Get the current user and their friends
    current_user = user_map[user_id]
    current_friends = set(current_user.get('friends', []))
    current_interests = set(current_user.get('interests', []))
    current_activity_level = current_user.get('activity', {}).get('level', None)

    # Determine recommendation mode
    mode = os.environ.get('RECOMMENDATION_MODE', 'basic').lower()
    if mode not in {'basic', 'enhanced', 'advanced'}:
        mode = 'basic'

    candidates = []
    for candidate_id, candidate in user_map.items():
        if candidate_id == user_id or candidate_id in current_friends:
            continue  # Skip self and existing friends

        candidate_friends = set(candidate.get('friends', []))
        candidate_interests = set(candidate.get('interests', []))
        candidate_activity_level = candidate.get('activity', {}).get('level', None)

        # Calculate mutual friends
        mutual_friends = len(current_friends & candidate_friends)

        # Basic mode: only mutual friends
        if mode == 'basic':
            score = float(mutual_friends)
        else:
            # Enhanced and advanced: add common interests
            common_interests = len(current_interests & candidate_interests)
            score = mutual_friends * 2.0 + common_interests * 1.5

            # Advanced: add bonus if activity levels match
            if mode == 'advanced' and current_activity_level and candidate_activity_level:
                if current_activity_level == candidate_activity_level:
                    score += 1.0

        if score > 0:
            candidates.append({'user_id': candidate_id, 'score': score})

    # Sort by score descending, then by user_id for deterministic output
    candidates.sort(key=lambda x: (-x['score'], x['user_id']))

    # Return top 5
    return candidates[:5]

# Ground-truth test from problem.json

import os

os.environ['RECOMMENDATION_MODE'] = 'basic'
result_basic = friend_suggestions('U001')
assert isinstance(result_basic, list)
assert len(result_basic) <= 5
for suggestion in result_basic:
    assert isinstance(suggestion, dict)
    assert 'user_id' in suggestion
    assert 'score' in suggestion
    assert isinstance(suggestion['score'], (int, float))
    assert suggestion['score'] > 0
    assert suggestion['user_id'] != 'U001'

# Test enhanced mode
os.environ['RECOMMENDATION_MODE'] = 'enhanced'
result_enhanced = friend_suggestions('U001')
assert isinstance(result_enhanced, list)
assert len(result_enhanced) <= 5
for suggestion in result_enhanced:
    assert 'user_id' in suggestion
    assert 'score' in suggestion

if result_basic and result_enhanced:
    assert result_enhanced[0]['score'] >= result_basic[0]['score'] * 0.8

# Test advanced mode
os.environ['RECOMMENDATION_MODE'] = 'advanced'
result_advanced = friend_suggestions('U001')
assert isinstance(result_advanced, list)
assert len(result_advanced) <= 5

# Test different user
os.environ['RECOMMENDATION_MODE'] = 'basic'
result_u002 = friend_suggestions('U002')
assert isinstance(result_u002, list)
assert len(result_u002) <= 5

print('Friend Suggester tests passed')

