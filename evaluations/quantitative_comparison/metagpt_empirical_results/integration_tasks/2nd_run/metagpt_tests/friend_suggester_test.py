# Add project root to path for imports
import sys
sys.path.insert(0, '/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent')

# Generated code by MetaGPT
import os
import json

def friend_suggestions(user_id):
    """
    Recommend friends for a user based on the social graph and RECOMMENDATION_MODE.
    Modes:
        - basic: score = number of mutual friends
        - enhanced: score = mutual friends * 2.0 + common interests * 1.5
        - advanced: enhanced + 1.0 bonus if activity level matches
    Returns: list of dicts [{user_id: ..., score: ...}], top 5 by score desc
    """
    # Load social graph
    with open("friend_suggester/social_graph.json", "r") as f:
        data = json.load(f)
    users = {u["user_id"]: u for u in data["users"]}
    if user_id not in users:
        return []

    mode = os.environ.get("RECOMMENDATION_MODE", "basic").lower()
    user = users[user_id]
    user_friends = set(user["friends"])
    user_interests = set(user.get("interests", []))
    user_activity = user.get("activity", {}).get("level", None)

    suggestions = []
    for candidate_id, candidate in users.items():
        if candidate_id == user_id or candidate_id in user_friends:
            continue  # Skip self and existing friends

        candidate_friends = set(candidate.get("friends", []))
        candidate_interests = set(candidate.get("interests", []))
        candidate_activity = candidate.get("activity", {}).get("level", None)

        # Mutual friends
        mutual = user_friends & candidate_friends
        mutual_count = len(mutual)

        # Common interests
        common_interests = user_interests & candidate_interests
        common_count = len(common_interests)

        score = 0.0
        if mode == "basic":
            score = float(mutual_count)
        elif mode == "enhanced":
            score = mutual_count * 2.0 + common_count * 1.5
        elif mode == "advanced":
            score = mutual_count * 2.0 + common_count * 1.5
            if user_activity and candidate_activity and user_activity == candidate_activity:
                score += 1.0
        else:
            score = float(mutual_count)  # fallback to basic

        if score > 0:
            suggestions.append({"user_id": candidate_id, "score": score})

    # Sort and return top 5
    suggestions.sort(key=lambda x: x["score"], reverse=True)
    return suggestions[:5]

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

