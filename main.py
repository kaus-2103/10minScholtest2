from fastapi import FastAPI, Request
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import chromadb
import requests

# === CONFIGURATION ===
CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "bangla_rag_knowledge_base_v3"
OLLAMA_MODEL = "mistral"
TOP_K = 3

# === INIT ===
print("🔧 Loading model and DB...")
model = SentenceTransformer("intfloat/multilingual-e5-base")
client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)

app = FastAPI()

# === REQUEST SCHEMA ===
class QueryRequest(BaseModel):
    question: str

# === HELPERS ===
def retrieve_chunks(query_text, top_k=TOP_K):
    query_embedding = model.encode(query_text)
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k,
        include=["documents", "distances"]
    )
    return results["documents"][0], results["distances"][0]

def build_prompt(question, context_chunks):
    context = "\n---\n".join(context_chunks)
    return f"""শুধুমাত্র নিচের তথ্য ব্যবহার করে প্রশ্নের উত্তর দাও। যদি উত্তর তথ্যের মধ্যে না পাও, তাহলে শুধুমাত্র বলো: 'উত্তর পাওয়া যায়নি'। অন্য কিছু বলো না।

তথ্য:
{context}

প্রশ্ন: {question}
উত্তর:"""


def ask_ollama(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}
    )
    return response.json().get("response", "উত্তর পাওয়া যায়নি।").strip()

# === API ROUTE ===
@app.post("/ask")
async def ask_question(data: QueryRequest):
    question = data.question.strip()
    chunks, distances = retrieve_chunks(question)
    prompt = build_prompt(question, chunks)
    answer = ask_ollama(prompt)
    return {
        "question": question,
        "top_chunks": [
            {"chunk": chunks[i], "score": distances[i]} for i in range(len(chunks))
        ],
        "answer": answer
    }
