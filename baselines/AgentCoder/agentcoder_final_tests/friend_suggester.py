
import json
import os

def friend_suggestions(user_id):
    '''
    Recommend friends for given user_id from social_graph.json using RECOMMENDATION_MODE:
    basic:           score = mutual friend count
    enhanced:        score = 2.0 * mutual friends + 1.5 * common interests
    advanced:        ... + 1.0 if activity levels match
    Returns: list of dicts [{user_id, score}], top 5 sorted desc
    '''
    # Step 1: Load data
    with open(os.path.join(os.path.dirname(__file__), 'social_graph.json'), encoding='utf-8') as f:
        data = json.load(f)
    user_map = {u['user_id']: u for u in data['users']}

    # Step 2: Get current user
    if user_id not in user_map:
        raise ValueError(f"No user with id {user_id}")
    user = user_map[user_id]
    user_friends = set(user['friends'])
    user_interests = set(user.get('interests', []))
    user_activity_level = user.get('activity', {}).get('level', '')

    # Step 3: Determine mode
    mode = os.environ.get('RECOMMENDATION_MODE', 'basic').lower()
    results = []
    
    for candidate_id, cand in user_map.items():
        if candidate_id == user_id or candidate_id in user_friends:
            continue
        
        # Mutual friends calculation
        cand_friends = set(cand.get('friends', []))
        mutual_friends = len(user_friends & cand_friends)

        # Basic mode
        score = mutual_friends

        # Enhanced mode
        if mode in ['enhanced', 'advanced']:
            cand_interests = set(cand.get('interests', []))
            common_interests = len(user_interests & cand_interests)
            score = 2.0 * mutual_friends + 1.5 * common_interests

            # Advanced mode: add activity level bonus
            if mode == 'advanced':
                cand_activity_level = cand.get('activity', {}).get('level', '')
                if cand_activity_level == user_activity_level and cand_activity_level != '':
                    score += 1.0

        results.append({'user_id': candidate_id, 'score': score})

    # Step 4: Sort and return top 5
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:5]



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
