import pandas as pd
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier

def train_pipeline(data_csv_path: str, model_pickle_path: str):
    if not os.path.exists(data_csv_path):
        raise FileNotFoundError(f"Missing training dataset at {data_csv_path}")
        
    df = pd.read_csv(data_csv_path)
    
    # Using TF-IDF as our ultra-lightweight text embedding model
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=1000)
    X = vectorizer.fit_transform(df['text'])
    y = df['label']
    
    # Use KNN classifier for lightning-fast inference (< 50MB footprint)
    knn = KNeighborsClassifier(n_neighbors=3, weights='distance')
    knn.fit(X, y)
    
    # Bundle components into a unified model package
    model_payload = {
        "vectorizer": vectorizer,
        "classifier": knn
    }
    
    os.makedirs(os.path.dirname(model_pickle_path), exist_ok=True)
    with open(model_pickle_path, 'wb') as f:
        pickle.dump(model_payload, f)
        
    size_mb = os.path.getsize(model_pickle_path) / (1024 * 1024)
    print(f"Model saved successfully. Total Size: {size_mb:.4f} MB (Target: < 50MB)")

if __name__ == "__main__":
    train_pipeline("../data/intents.csv", "./model.pkl")
