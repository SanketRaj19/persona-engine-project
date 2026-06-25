import sys
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Inject workspace paths for inner modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../intent_classifier')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../rag_resolver')))

from classifier import OfflineIntentClassifier
from resolver import RagResolver

router = APIRouter()

# Initialize Engine Singletons
classifier = OfflineIntentClassifier(model_path=os.path.abspath(os.path.join(os.path.dirname(__file__), "../intent_classifier/model.pkl")))
rag_resolver = RagResolver(db_dir=os.path.abspath(os.path.join(os.path.dirname(__file__), "../rag_resolver/chroma_db")))

class MessageRequest(BaseModel):
    message: str

class QueryRequest(BaseModel):
    query: str

@router.post("/classify")
async def classify_intent(payload: MessageRequest):
    try:
        label, score = classifier.predict(payload.message)
        return {"intent": label, "confidence": score}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/resolve-rag")
async def resolve_rag_query(payload: QueryRequest):
    try:
        answer = rag_resolver.resolve_query(payload.query)
        return {"response": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
