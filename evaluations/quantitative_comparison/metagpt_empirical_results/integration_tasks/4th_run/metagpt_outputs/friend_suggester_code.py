import os
import json

def friend_suggestions(user_id):
    """
    Recommend friends for a user based on mutual friends, common interests, and activity level.
    Uses RECOMMENDATION_MODE environment variable to determine scoring mode.
    Returns top 5 suggestions as a list of dicts with user_id and score.
    """
    # Load social graph data
    data_path = os.path.join(os.path.dirname(__file__), "social_graph.json")
    with open(data_path, "r", encoding="utf-8") as f:
        social_graph = json.load(f)

    users = social_graph["users"]
    user_map = {user["user_id"]: user for user in users}

    if user_id not in user_map:
        raise ValueError(f"user_id '{user_id}' not found in social graph.")

    # Get current user info
    current_user = user_map[user_id]
    current_friends = set(current_user["friends"])
    current_interests = set(current_user.get("interests", []))
    current_activity_level = current_user.get("activity", {}).get("level", None)

    # Candidates: all users except self and current friends
    candidate_ids = set(user_map.keys()) - current_friends - {user_id}

    # Get recommendation mode
    mode = os.environ.get("RECOMMENDATION_MODE", "basic").lower()
    if mode not in {"basic", "enhanced", "advanced"}:
        mode = "basic"

    suggestions = []

    for candidate_id in candidate_ids:
        candidate = user_map[candidate_id]
        candidate_friends = set(candidate.get("friends", []))
        candidate_interests = set(candidate.get("interests", []))
        candidate_activity_level = candidate.get("activity", {}).get("level", None)

        # Mutual friends
        mutual_friends = current_friends & candidate_friends
        num_mutual_friends = len(mutual_friends)

        # Common interests
        num_common_interests = len(current_interests & candidate_interests)

        # Activity level match
        activity_match = (
            1.0 if (mode == "advanced" and current_activity_level == candidate_activity_level and current_activity_level is not None) else 0.0
        )

        # Scoring
        if mode == "basic":
            score = num_mutual_friends
        elif mode == "enhanced":
            score = num_mutual_friends * 2.0 + num_common_interests * 1.5
        elif mode == "advanced":
            score = num_mutual_friends * 2.0 + num_common_interests * 1.5 + activity_match
        else:
            score = num_mutual_friends  # fallback

        if score > 0:
            suggestions.append({"user_id": candidate_id, "score": score})

    # Sort by score descending, then by user_id for deterministic output
    suggestions.sort(key=lambda x: (-x["score"], x["user_id"]))

    # Return top 5
    return suggestions[:5]