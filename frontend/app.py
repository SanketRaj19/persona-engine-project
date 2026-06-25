import streamlit as st
import requests
import json
import os

st.set_page_config(page_title="Persona Engine UI", layout="wide")
st.title("Persona Engine Dashboard Console")

BACKEND_URL = "http://127.0.0.1:8000/api/v1"

tab1, tab2, tab3, tab4 = st.tabs(["Drift Monitor", "Offline Intent Classifier", "RAG Conflict Resolver", "System Design View"])

with tab1:
    st.header("Daily Persona Drift Timeline")
    timeline_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/timeline.json"))
    
    if os.path.exists(timeline_path):
        with open(timeline_path, 'r') as f:
            timeline_data = json.load(f)
        st.json(timeline_data)
    else:
        st.info("No active baseline timeline file found. Run Drift Engine pipeline to view.")

with tab2:
    st.header("Real-time Offline Intent Inference")
    user_input = st.text_input("Enter message string to route:")
    if st.button("Evaluate Intent"):
        if user_input:
            res = requests.post(f"{BACKEND_URL}/classify", json={"message": user_input})
            if res.status_code == 200:
                st.success(f"Classification Result: {res.json()}")
            else:
                st.error("Error connecting to localized inference API.")

with tab3:
    st.header("RAG Context Conflict Resolver")
    rag_input = st.text_input("Query personal history storage matrix:")
    if st.button("Query Vector Space"):
        if rag_input:
            res = requests.post(f"{BACKEND_URL}/resolve-rag", json={"query": rag_input})
            if res.status_code == 200:
                st.info(res.json()["response"])
            else:
                st.error("Error executing vector lookups.")

with tab4:
    st.header("Architecture Specification")
    doc_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../docs/design.md"))
    if os.path.exists(doc_path):
        with open(doc_path, 'r') as f:
            st.markdown(f.read())
