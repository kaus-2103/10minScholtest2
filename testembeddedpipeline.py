from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

# Initialize model
model = SentenceTransformer('distiluse-base-multilingual-cased-v2')

# Initialize ChromaDB (local) using PersistentClient
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(name="bangla_rag_knowledge_base")


# Load cleaned chunks
def load_chunks(file_path):
    chunks = []
    with open(file_path, "r", encoding="utf-8") as f:
        data = f.read()
        raw_chunks = data.split("=" * 50)
        for block in raw_chunks:
            if block.strip():
                chunks.append(block.strip())
    return chunks


# Embed and store chunks
def index_chunks(chunks):
    for idx, chunk in enumerate(chunks):
        embedding = model.encode(chunk)
        collection.add(
            ids=[f"chunk_{idx}"],
            documents=[chunk],
            embeddings=[embedding.tolist()]  # Convert numpy array to list
        )
        print(f"Indexed chunk_{idx}")


if __name__ == "__main__":
    chunks = load_chunks("data\cleaned_chunked_output.txt")
    index_chunks(chunks)
    print("Embedding & indexing completed.")
    
