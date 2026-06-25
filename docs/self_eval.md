# Sprint Self-Evaluation

## What Went Well
- **Offline Constraints Met**: The KNN model baseline takes up less than 5MB of disk space, drastically beating the 50MB budget constraint. Latency averages ~12ms on baseline CPU hardware, well below the 200ms threshold.
- **RAG Scoring Algorithm**: The hybrid math scoring algorithm effectively weighs freshness alongside intense emotional metrics to resolve conflicting data.

## Challenges & Trade-offs
- **VADER Granularity**: The standard VADER analyzer handles core sentiments beautifully but struggles with extremely subtle context shifts (like sarcasm). Upgrading to a custom token-based rule array helped isolate specific trigger words.
