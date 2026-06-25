from typing import List, Dict, Any, Tuple

class ContradictionDetector:
    """
    Evaluates contextual conflict boundaries by analyzing vocabulary overlap
    and opposite semantic directions across high-scoring chunks.
    """
    def check_for_contradictions(self, ranked_chunks: List[Dict[str, Any]]) -> List[Tuple[Dict[str, Any], Dict[str, Any]]]:
        contradictions = []
        if len(ranked_chunks) < 2:
            return contradictions
            
        # Quick lookahead search loop comparing content vectors/words
        for i in range(len(ranked_chunks)):
            for j in range(i + 1, len(ranked_chunks)):
                c1 = ranked_chunks[i]
                c2 = ranked_chunks[j]
                
                txt1 = c1["text"].lower()
                txt2 = c2["text"].lower()
                
                # Check conflict patterns (e.g., "loves her" vs "estranged", "lives with" vs "moved away")
                conflict_signals = [
                    ("lives with", "moved"), ("married", "divorced"), 
                    ("close", "distant"), ("estranged", "close"),
                    ("only sibling", "half-sister")
                ]
                
                for word_a, word_b in conflict_signals:
                    if (word_a in txt1 and word_b in txt2) or (word_b in txt1 and word_a in txt2):
                        contradictions.append((c1, c2))
                        
        return contradictions
