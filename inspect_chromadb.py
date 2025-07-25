# inspect_chromadb.py

from sentence_transformers import SentenceTransformer
import chromadb

# === Configuration ===
CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "bangla_rag_knowledge_base_v3"
TOP_K = 3

# === Initialize Model & DB ===
model = SentenceTransformer("intfloat/multilingual-e5-base")
client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)

# === Show Total Chunks Stored ===
print(f"📦 Total Chunks in Collection: {collection.count()}")

# === Peek at Stored Chunks ===
print("\n🔍 Peeking at sample chunks (up to 5):")
results = collection.peek()
for i, doc in enumerate(results["documents"][:5]):
    print(f"\nChunk {i+1}:")
    print(doc)
    print("-" * 60)

# === Test with Multiple Queries ===
test_queries = [
    "অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?",
    "কাকে অনুপমের ভাগ্য দেবতা বলে উল্লেখ করা হয়েছে?",
    "বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?"
]

print("\n\n🔎 Running test queries...\n")
for q in test_queries:
    print(f"\n🧠 Query: {q}")
    query_embedding = model.encode(q)

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=TOP_K,
        include=["documents", "distances"]
    )

    for i in range(TOP_K):
        print(f"\n🔹 Match {i+1}:")
        print(f"📄 Text: {results['documents'][0][i]}")
        print(f"📏 Distance: {results['distances'][0][i]:.4f}")
        print("-" * 50)

# === Optional: Show All Chunk IDs ===
print("\n📋 Stored Chunk IDs (first 10):")
print(results["ids"][0][:10])
