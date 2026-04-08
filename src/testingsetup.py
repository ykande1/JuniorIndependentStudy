import chromadb
from sentence_transformers import SentenceTransformer
import ollama

print("✅ Libraries loaded.")

# Check MiniLM
model = SentenceTransformer('all-MiniLM-L6-v2')
print("✅ Embedding model ready.")

# Check Ollama 
response = ollama.chat(model='phi3', messages=[{'role': 'user', 'content': 'Say "Ready!"'}])
print(f"✅ AI Response: {response['message']['content']}")