from typing import List, Dict, Any

class ChunkRanker:
    @staticmethod
    def calculate_score(chunk: Dict[str, Any], max_day: int) -> float:
        """
        Applies mathematical scoring blending freshness values and text intensity weights.
        Score = (day / max_day) * 0.6 + (emotional_weight) * 0.4
        """
        metadata = chunk.get("metadata", {})
        day = metadata.get("day", 1)
        emotional_weight = metadata.get("emotional_weight", 0.0)
        
        # Normalize relative day progression weight
        recency_score = day / max_day if max_day > 0 else 1.0
        
        # Formula composition
        final_score = (recency_score * 0.6) + (emotional_weight * 0.4)
        return final_score

    def rank_retrieved_chunks(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not chunks:
            return []
            
        max_day = max([c.get("metadata", {}).get("day", 1) for c in chunks])
        
        for chunk in chunks:
            chunk["combined_score"] = self.calculate_score(chunk, max_day)
            
        # Return chunks sorted by high composite priority score
        return sorted(chunks, key=lambda x: x["combined_score"], reverse=True)
