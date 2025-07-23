from sentence_transformers import SentenceTransformer
import chromadb

# Load model & ChromaDB
model = SentenceTransformer('distiluse-base-multilingual-cased-v2')
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="bangla_rag_knowledge_base")

# Semantic search function
def query_knowledge_base(query, top_k=3):
    query_embedding = model.encode(query)
    
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )

    print(f"🔍 Top {top_k} results for query: \"{query}\"")
    for i, doc in enumerate(results['documents'][0]):
        print(f"\n📄 Match {i+1}:")
        print(doc)
        print("-" * 50)

# EXAMPLE USAGE
if __name__ == "__main__":
    query = input("Enter your question in Bangla or English: ")
    query_knowledge_base(query)
