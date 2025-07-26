# rag_api.py

from fastapi import FastAPI, Request
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import chromadb
import requests
from typing import List, Dict
from uuid import uuid4

# === CONFIG ===
CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "bangla_rag_knowledge_base_v3"
OLLAMA_MODEL = "mistral"
TOP_K = 3
MAX_MEMORY = 5

# === INIT ===
app = FastAPI()
model = SentenceTransformer("intfloat/multilingual-e5-base")
client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)
session_memory: Dict[str, List[Dict[str, str]]] = {}

# === Input Schema ===
class QueryInput(BaseModel):
    question: str
    session_id: str = None  # optional, auto-generated if not provided

# === Core Functions ===
def retrieve_chunks(query_text, top_k=TOP_K):
    query_embedding = model.encode(query_text)
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k,
        include=["documents", "distances"]
    )
    return results["documents"][0], results["distances"][0]

def build_prompt(question: str, context_chunks: List[str], memory_items: List[Dict[str, str]]):
    context = "\n---\n".join(context_chunks)
    memory_block = "\n".join([f"প্রশ্ন: {item['q']}\nউত্তর: {item['a']}" for item in memory_items])
    return f"""তুমি একটি বাংলা প্রশ্ন-উত্তরকারী সহকারী। নিচের তথ্য ব্যবহার করে প্রশ্নের উত্তর দাও। যদি প্রাসঙ্গিক তথ্য না পাও, বলো "উত্তর পাওয়া যায়নি"।

প্রাসঙ্গিক চাঙ্ক:
{context}

পূর্ববর্তী প্রশ্নোত্তর:
{memory_block}

বর্তমান প্রশ্ন: {question}
উত্তর:"""

def ask_ollama(prompt: str):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}
    )
    return response.json()["response"].strip()

# === API Route ===
@app.post("/ask")
def ask_question(query: QueryInput):
    session_id = query.session_id or str(uuid4())

    # Retrieve memory for the session
    memory = session_memory.get(session_id, [])

    # Fetch context from ChromaDB
    chunks, scores = retrieve_chunks(query.question)

    # Build prompt with memory + retrieved chunks
    prompt = build_prompt(query.question, chunks, memory[-MAX_MEMORY:])

    # Generate answer
    answer = ask_ollama(prompt)

    # Store Q&A in memory
    memory.append({"q": query.question, "a": answer})
    session_memory[session_id] = memory[-MAX_MEMORY:]

    return {
        "session_id": session_id,
        "question": query.question,
        "answer": answer,
        "top_chunks": [{"chunk": chunk, "score": float(score)} for chunk, score in zip(chunks, scores)]
    }
