# 🤖 Adaptive Persona Engine & Offline Intent Classifier

A local-first, privacy-focused intelligent assistant middleware framework designed to track long-term persona drift patterns, route intents entirely offline on CPU in sub-200ms windows, and dynamically mitigate retrieval conflicts in a RAG pipeline.

---

## 🏗️ Architecture & Component Layout

The workspace is organized into functional micro-modules corresponding to execution timelines:

* **`persona_drift/`**: Aggregates conversation contexts, processes sentiment scores via VADER, evaluates daily keyword weights using TF-IDF, and maps behavioral persona shifts over time.
* **`intent_classifier/`**: An offline-first inference layout operating via a highly-optimized KNN configuration vectorizer (<5MB footprint, ~12ms execution latency window).
* **`rag_resolver/`**: A vector-retrieval pipeline powered by ChromaDB designed to resolve historical context conflicts by blending text freshness and emotional parameters.
* **`api/` & `frontend/`**: FastAPI backend infrastructure coupled with a web-based Streamlit administration dashboard dashboard console.

---

## 🛠️ Requirements & System Setup

Ensure you have Python 3.9+ installed on your local computer machine. Follow these execution commands to provision environment spaces and system packages.

### 1. Installation
Navigate into the project root directory and run:

```bash
pip install fastapi uvicorn scikit-learn pandas nltk chromadb streamlit pydantic requests

#step-1
cd intent_classifier
python generate_data.py
python train.py
python benchmark.py

#step-2
cd ../rag_resolver
python ingest.py

#step-3
cd ../persona_drift
python drift_engine.py

#step-4
cd ../api
python main.py

cd frontend
streamlit run app.py
