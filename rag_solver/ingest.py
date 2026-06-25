import json
import os
import chromadb
from chromadb.utils import embedding_functions

def ingest_persona_data(json_input_path: str, db_dir: str):
    if not os.path.exists(json_input_path):
        raise FileNotFoundError(f"Source JSON file missing at {json_input_path}")
        
    with open(json_input_path, 'r') as f:
        data = json.load(f)
        
    # Initialize light, local ChromaDB instance 
    client = chromadb.PersistentClient(path=db_dir)
    
    # Use standard default sentence-transformers or lightweight default internal math embeddings
    collection = client.get_or_create_collection(name="persona_checkpoints")
    
    # Expecting: {"checkpoints": [{"id": "cp1", "text": "...", "day": 1, "emotional_weight": 0.8}, ...]}
    checkpoints = data.get("checkpoints", [])
    
    ids = []
    documents = []
    metadatas = []
    
    for cp in checkpoints:
        ids.append(str(cp["id"]))
        documents.append(cp["text"])
        metadatas.append({
            "day": int(cp["day"]),
            "emotional_weight": float(cp["emotional_weight"])
        })
        
    if ids:
        collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
    print(f"Successfully ingested {len(ids)} text checkpoints into ChromaDB vector space.")

if __name__ == "__main__":
    ingest_persona_data("../data/persona.json", "./chroma_db")
