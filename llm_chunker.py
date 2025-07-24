# llm_chunker.py

import requests
from sentence_transformers import SentenceTransformer
import chromadb
import time

# === Config ===
OLLAMA_MODEL = "mistral"  # Make sure you have `ollama pull mistral`
INPUT_FILE = "data/ocr_bangla_output.txt"
CHUNKED_OUTPUT_FILE = "data/cleaned_chunked_output.txt"
CHROMA_DB_PATH = "./chroma_db"
CHROMA_COLLECTION_NAME = "bangla_rag_kb_llm"

# === Load Full Text ===
def load_full_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# === Send to Ollama for Chunking ===
def chunk_with_ollama(text):
    print("🤖 Sending text to Ollama for chunking...")
    prompt = f"""
    Chunked the text into manageable pieces for RAG (Retrieval-Augmented Generation) purposes.
লেখা:
{text}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    output = response.json().get("response", "").strip()
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }
    )
    
    output = response.json().get("response", "").strip()
    print("🧾 LLM Raw Output Preview:\n", output[:1000])
    return output

# === Save Chunked Output to File ===
def save_chunked_output(text, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"📁 Chunked output saved to {path}")

# === Process Chunked Text into List ===
def parse_chunks(text):
    raw_chunks = text.split("======")
    return [chunk.strip() for chunk in raw_chunks if chunk.strip()]

# === Embed and Store into New ChromaDB ===
def store_chunks_in_chromadb(chunks):
    print("🔧 Initializing ChromaDB (new collection)...")
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = client.get_or_create_collection(name=CHROMA_COLLECTION_NAME)

    model = SentenceTransformer('intfloat/multilingual-e5-base')
    print("📦 Embedding and indexing chunks...")

    for idx, chunk in enumerate(chunks):
        embedding = model.encode(chunk)
        collection.add(
            ids=[f"llm_chunk_{idx}"],
            documents=[chunk],
            embeddings=[embedding.tolist()]
        )
        print(f"✅ Indexed llm_chunk_{idx}")
        time.sleep(0.1)  # avoid overloading

    print("🎉 All LLM-chunks stored in ChromaDB!")

# === Main ===
if __name__ == "__main__":
    print("📥 Loading original OCR output...")
    original_text = load_full_text(INPUT_FILE)

    chunked_text = chunk_with_ollama(original_text)
    save_chunked_output(chunked_text, CHUNKED_OUTPUT_FILE)

    chunks = parse_chunks(chunked_text)
    print(f"📚 Total LLM chunks: {len(chunks)}")

    store_chunks_in_chromadb(chunks)
