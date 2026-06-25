# Local-First Sync Architecture (Adaptive Persona Engine)

## 1. System Architecture Diagram

+---------------------------------------------------------------------------------+
|                                 CLIENT DEVICE                                   |
|                                                                                 |
|  +--------------------+      +--------------------+      +-------------------+  |
|  |    Streamlit UI    | ---> |  FastAPI App Glue  | ---> |   SQLite Local    |  |
|  +--------------------+      +--------------------+      +--+----------------+  |
|                                                             |                   |
|                                  +-----------------------+  |                   |
|                                  | ChromaDB Vector Store |<-+ (Local Checkpoint)|
|                                  +-----------------------+                      |
+-------------------------------------------------------------|-------------------+
| Secure TLS
v WebSockets/HTTPS
+---------------------------------------------------------------------------------+
|                                REMOTE REPOSITORY                                |
|                                                                                 |
|  +--------------------+      +--------------------+      +-------------------+  |
|  | Sync Workers / Queue| ---> | Central Engine API | ---> | Cloud PostgreSQL  |  |
|  +--------------------+      +--------------------+      +-------------------+  |
+---------------------------------------------------------------------------------+


## 2. Core Execution Topology

### On-Device Cache Layer
* **Storage Footprint:** **SQLite** holds structural records (user chats, timeline telemetry parameters); **ChromaDB Vector Store** handles contextual search blocks locally on-device.
* **Security Isolation:** Embedding actions run locally on CPU. Raw chat strings remain enclosed within client sandboxes to preserve zero-exposure user confidentiality.

### Synchronization Rules Engine
* **What Syncs Local to Cloud:** Aggregated persona timeline metadata models (e.g., parsed anonymous daily parameters: `{"day": 7, "tone": "playful", "trigger_id": 104}`) and offline intent distribution summaries.
* **What Stays Local:** Fully un-redacted personal conversation records, baseline dictionary matrix definitions, and raw embeddings vectors.

## 3. Concurrency & Conflict Resolution Strategy

The platform maintains tracking with a **Last-Write-Wins + Vector Clock Verification Matrix**. 

* If data modifications conflict across devices on identical timeline intervals, the database checks structural entry hashes. 
* It selects the entry with the higher chronological vector state step value. 
* If states perfectly clash, it falls back to a deterministic metric evaluation function: it retains the log entry that exhibits a higher structural emotional value weight to guarantee that critical user context signals are never lost during sync cycles.
