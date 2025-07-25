from sentence_transformers import SentenceTransformer
import chromadb

# === Load Model ===
model = SentenceTransformer('intfloat/multilingual-e5-base')  # Works with Bangla

# === Initialize ChromaDB (Persistent) ===
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="bangla_rag_knowledge_base_v3") # bangla_rag_knowledge_base_v2 and bangla_rag_knowledge_base_v failed

# === Load Chunks from File ===
def load_chunks(file_path):
    chunks = []
    with open(file_path, "r", encoding="utf-8") as f:
        data = f.read()
        raw_chunks = data.split("=" * 50)  # Split by chunk divider
        for block in raw_chunks:
            if block.strip():
                chunks.append(block.strip())
    return chunks

# === Index Chunks into ChromaDB ===
def index_chunks(chunks):
    for idx, chunk in enumerate(chunks):
        embedding = model.encode(chunk)
        collection.add(
            ids=[f"chunk_{idx}"],
            documents=[chunk],
            embeddings=[embedding.tolist()]  # Chroma requires lists
        )
        print(f"✅ Indexed chunk_{idx}")
    print("🎉 All chunks embedded and stored.")

# === MAIN EXECUTION ===
if __name__ == "__main__":
    chunks = load_chunks("data/merged.txt")
    print(f"📦 Loaded {len(chunks)} chunks from file.")
    index_chunks(chunks)
