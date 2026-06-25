import chromadb
from ranker import ChunkRanker
from contradiction import ContradictionDetector

class RagResolver:
    def __init__(self, db_dir: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(path=db_dir)
        self.collection = self.client.get_collection(name="persona_checkpoints")
        self.ranker = ChunkRanker()
        self.detector = ContradictionDetector()

    def resolve_query(self, query_text: str) -> str:
        # 1. Vector Search Query Fetching 
        results = self.collection.query(query_texts=[query_text], n_results=5)
        
        if not results or not results["documents"][0]:
            return "No matching persona information checkpoints found."
            
        # Reformat context records
        chunks = []
        for idx in range(len(results["documents"][0])):
            chunks.append({
                "id": results["ids"][0][idx],
                "text": results["documents"][0][idx],
                "metadata": results["metadatas"][0][idx]
            })
            
        # 2. Run Ranker Pipeline
        ranked = self.ranker.rank_retrieved_chunks(chunks)
        
        # 3. Detect Internal Contradictions
        conflicts = self.detector.check_for_contradictions(ranked)
        
        # 4. Synthesize Merged Coherent Answer
        top_match = ranked[0]
        
        if conflicts:
            conflict_log = []
            for c1, c2 in conflicts:
                conflict_log.append(
                    f"[Conflict Found: Day {c1['metadata']['day']} says '{c1['text']}' vs Day {c2['metadata']['day']} which says '{c2['text']}']"
                )
            
            resolution_prefix = "⚠️ Contextual contradictions resolved by recency & emotion ranking metrics.\n"
            merged_response = (
                f"{resolution_prefix}"
                f"Most credible current data (Day {top_match['metadata']['day']}): \"{top_match['text']}\".\n"
                f"Historical Context Changes Observed:\n" + "\n".join(conflict_log)
            )
            return merged_response
            
        return f"Verified Persona Context: \"{top_match['text']}\" (Recorded on Day {top_match['metadata']['day']})."

if __name__ == "__main__":
    resolver = RagResolver()
    print(resolver.resolve_query("Did I mention anything about my sister?"))
