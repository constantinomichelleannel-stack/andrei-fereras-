from typing import List, Tuple

def predict_probability(case_facts: str) -> Tuple[float, List[str]]:
    lower = case_facts.lower()
    factors = []
    score = 0.5
    if 'precedent' in lower:
        score += 0.1; factors.append('Relevant precedent cited (+0.1)')
    if 'jurisdiction' in lower:
        score += 0.05; factors.append('Jurisdiction clarified (+0.05)')
    if 'weak evidence' in lower:
        score -= 0.2; factors.append('Weak evidence (-0.2)')
    if 'settlement' in lower:
        score += 0.05; factors.append('Willingness to settle (+0.05)')
    score = max(0.01, min(0.99, score))
    return score, factors
