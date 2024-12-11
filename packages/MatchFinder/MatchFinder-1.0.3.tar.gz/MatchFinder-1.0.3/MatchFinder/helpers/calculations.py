from .._internal.core import calculate_similarity_score

def find_matches(input_str, match_list, n=3, include_score=False):
    """
    Find close matches based on similarity scores.
    """
    scores = [(item, calculate_similarity_score(input_str, item)) for item in match_list]
    sorted_matches = sorted(scores, key=lambda x: x[1], reverse=True)
    top_matches = sorted_matches[:n]

    if include_score:
        return [{"match": match, "score": round(score, 2)} for match, score in top_matches]
    else:
        return [{"match": match} for match, _ in top_matches]
