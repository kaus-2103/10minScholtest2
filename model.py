# rag_ollama.py

import chromadb
import requests
from sentence_transformers import SentenceTransformer

# === CONFIGURATION ===
CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "bangla_rag_knowledge_base_v3" # bangla_rag_knowledge_base_v and bangla_rag_knowledge_base_v2 failed
OLLAMA_MODEL = "mistral"
TOP_K = 3

# === INITIALIZE EMBEDDING MODEL & CHROMADB ===
print("🔧 Loading embedding model...")
model = SentenceTransformer("intfloat/multilingual-e5-base")

print("🔧 Connecting to ChromaDB...")
client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)

# === FUNCTION: Query ChromaDB for Top-K Relevant Chunks ===
def retrieve_chunks(query_text, top_k=TOP_K):
    query_embedding = model.encode(query_text)
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k,
        include=["documents", "distances"]
    )
    return results["documents"][0], results["distances"][0]

# === FUNCTION: Format Prompt for Ollama LLM ===
def build_prompt(question, context_chunks):
    context = "\n---\n".join(context_chunks)
    return f"""প্রশ্নের উত্তর দাও শুধুমাত্র নিচের তথ্য ব্যবহার করে। যদি তথ্য না পাও, বলো 'উত্তর পাওয়া যায়নি'।

প্রসঙ্গ:
{context}

প্রশ্ন: {question}
উত্তর:"""

# === FUNCTION: Call Ollama Local Model ===
# def ask_ollama(prompt):
#     response = requests.post(
#         "http://localhost:11434/api/generate",
#         json={
#             "model": OLLAMA_MODEL,
#             "prompt": prompt,
#             "stream": False
#         }
#     )
#     return response.json()["response"].strip()

def ask_ollama(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }
    )
    # print("📤 Raw response from Ollama:", response.json())  # bugger
    return response.json()["response"].strip()

# === MAIN RUNNER ===
if __name__ == "__main__":
    print("\n🤖 Bengali RAG Answer Generator (Local LLM + ChromaDB)\n")

    while True:
        user_question = input("❓ আপনার প্রশ্ন লিখুন (exit লিখে বন্ধ করুন): ").strip()
        if user_question.lower() in ["exit", "quit"]:
            break

        print("\n🔍 প্রশ্ন বিশ্লেষণ হচ্ছে...\n")
        chunks, distances = retrieve_chunks(user_question)

        print("📚 প্রাসঙ্গিক তথ্যাংশ (Top Chunks):\n")
        for i, chunk in enumerate(chunks):
            print(f"[Chunk {i+1}] (Similarity Score: {distances[i]:.4f})\n{chunk}\n{'-'*60}")

        prompt = build_prompt(user_question, chunks)
        print("\n🤖 উত্তর তৈরি হচ্ছে...\n")
        answer = ask_ollama(prompt)

        print(f"\n✅ LLM এর উত্তর:\n{answer}\n{'='*60}\n")
