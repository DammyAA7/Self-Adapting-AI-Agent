import os
import json

def friend_suggestions(user_id):
    """
    Recommend friends for a given user_id based on social_graph.json and RECOMMENDATION_MODE.
    Returns a list of dicts: [{'user_id': ..., 'score': ...}, ...] sorted by score descending, top 5 only.
    """
    # Load social graph
    with open(os.path.join(os.path.dirname(__file__), "social_graph.json"), "r") as f:
        data = json.load(f)
    users = {u["user_id"]: u for u in data["users"]}
    if user_id not in users:
        return []

    user = users[user_id]
    user_friends = set(user["friends"])
    user_interests = set(user.get("interests", []))
    user_activity = user.get("activity", {}).get("level", None)

    mode = os.environ.get("RECOMMENDATION_MODE", "basic").lower()
    suggestions = []

    for candidate_id, candidate in users.items():
        if candidate_id == user_id or candidate_id in user_friends:
            continue  # Skip self and existing friends

        candidate_friends = set(candidate.get("friends", []))
        candidate_interests = set(candidate.get("interests", []))
        candidate_activity = candidate.get("activity", {}).get("level", None)

        # Mutual friends
        mutual_friends = user_friends & candidate_friends
        mutual_count = len(mutual_friends)

        # Common interests
        common_interests = user_interests & candidate_interests
        interests_count = len(common_interests)

        # Scoring
        if mode == "basic":
            score = mutual_count
        elif mode == "enhanced":
            score = mutual_count * 2.0 + interests_count * 1.5
        elif mode == "advanced":
            score = mutual_count * 2.0 + interests_count * 1.5
            if user_activity and candidate_activity and user_activity == candidate_activity:
                score += 1.0
        else:
            score = mutual_count  # fallback to basic

        if score > 0:
            suggestions.append({"user_id": candidate_id, "score": score})

    # Sort and return top 5
    suggestions.sort(key=lambda x: x["score"], reverse=True)
    return suggestions[:5]