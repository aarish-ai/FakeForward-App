from typing import List, Tuple
from backend.models import ClaimResult

def aggregate_verdict(claims: List[ClaimResult]) -> Tuple[str, int]:
    """
    Aggregates the individual claim verdicts into an overall verdict and score.
    Returns (verdict, average_score).
    """
    if not claims:
        return "NO_CLAIMS_FOUND", 0
        
    all_unverifiable = all(c.verdict == "UNVERIFIABLE" for c in claims)
    if all_unverifiable:
        return "UNVERIFIABLE", 50
        
    total_score = sum(c.score for c in claims)
    avg_score = int(total_score / len(claims))
    
    if avg_score >= 80:
        return "TRUE", avg_score
    elif avg_score >= 40:
        return "PROBABLE", avg_score
    else:
        return "FALSE", avg_score
