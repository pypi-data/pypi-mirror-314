from typing import List, Optional, Tuple
from Levenshtein import distance

def find_closest_match(input_str: str, valid_options: List[str], threshold: float = 0.5) -> Optional[Tuple[str, float]]:
    """
    Find the closest matching string from a list of valid options using Levenshtein distance.
    
    Args:
        input_str: The input string to match
        valid_options: List of valid string options to match against
        threshold: Minimum similarity score (0-1) required for a match
        
    Returns:
        Tuple of (closest_match, similarity_score) if a match is found above threshold
        None if no match meets the threshold
    """
    if not input_str or not valid_options:
        return None
        
    input_upper = input_str.upper()
    best_match = None
    best_score = 0
    
    for option in valid_options:
        option_upper = option.upper()
        dist = distance(input_upper, option_upper)
        max_len = max(len(input_upper), len(option_upper))
        score = 1 - (dist / max_len)
        
        if score > best_score:
            best_score = score
            best_match = option
            
    if best_score >= threshold:
        return (best_match, best_score)
    return None

def validate_billing_granularity(input_value: str) -> Optional[str]:
    """
    Validate billing granularity input with fuzzy matching.
    
    Args:
        input_value: The input billing granularity string
        
    Returns:
        Matched valid billing granularity if found, None otherwise
    """
    VALID_GRANULARITIES = [
        "PER_SECOND",
        "PER_MINUTE", 
        "PER_HOUR",
        "PER_10_MINUTES"
    ]
    
    result = find_closest_match(input_value, VALID_GRANULARITIES)
    return result[0] if result else None
