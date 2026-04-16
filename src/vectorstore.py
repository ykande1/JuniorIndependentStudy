import json
import chromadb
from chromadb.utils import embedding_functions

# Initialize Local ChromaDB (Issue #3)
# This creates a folder called 'esrs_db' to store the data permanently.
client = chromadb.PersistentClient(path="./data/esrs_db")


#all-MiniLM-L6-v2 takes the chunk of text and converts it into a vector of numbers that captures the meaning of the text. This allows us to compare different chunks based on their meaning.
embedding_model = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")


#specific table in the database, we name it esrs_docs and tell it to use the translator model we just picked. 
collection = client.get_or_create_collection(
    name="esrs_docs", 
    embedding_function =    embedding_model
)

# Load and Store Chunks (Issue #3)
with open("./data/processed/master_esrs.json", "r") as f:
    chunks = json.load(f)

# ChromaDB likes data in lists
documents = [c["text"] for c in chunks] 
metadatas = [{"source": c["source"], "page": c["page"], "section": c["section"], "type": c["type"]} for c in chunks]
ids = [f"id_{i}" for i in range(len(chunks))]

collection.add(documents=documents, metadatas=metadatas, ids=ids)
print(f"Successfully indexed {len(chunks)} chunks into ChromaDB.")

# Implement Retrieval (Issue #4)
def retrieve_context(query):
    results = collection.query(
        query_texts=[query],
        n_results=5  # Top-k retrieval
    )
    return results['documents'][0], results['metadatas'][0]

# --- TEST IT ---
#test_query = "What is the objective of ESRS E1?"
#docs, meta = retrieve_context(test_query)
#print(f"\nTop Match: {docs[0]}\nSource: {meta[0]['source']} (Page {meta[0]['page']})")
#What are the requirements for ESRS E1-6 regarding Gross Scope 3 GHG emissions? 