import ollama
from vectorstore import retrieve_context

def ask_esrs_assistant(query):
    # 1. Get relevant chunks from Vector Database
    docs, metadatas = retrieve_context(query)
    
    # Combine the retrieved chunks into one big string of text
    context_text = "\n\n".join(docs)
    
    # Grounded System Prompt (Issue #5)
    system_prompt = f"""
    You are a professional assistant specializing in European Sustainability Reporting Standards (ESRS).
    Your goal is to answer the user's question using ONLY the provided legal context below.
    
    RULES:
    1. Only use the provided CONTEXT to answer. 
    2. IGNORE your internal memory about the ESRS document names or page numbers.
    3. If you cite a source, you MUST use the 'Source' and 'Page' exactly as they appear in the metadata I provide.
    4. If the answer is not contained within the CONTEXT, strictly state: "I'm sorry, but the provided ESRS documents do not contain information to answer that question."
    5. Do not use outside knowledge or make up facts.
    6. Be Concise, try to answer in LESS THAN 5 sentences. 
    7. If the answer includes a list, use bullet points. 
 

    "STRICT RULE: Do not mention any book titles, organizations, or page numbers that are not explicitly written in the provided CONTEXT. Only use the 'Source' and 'Page' provided in the metadata."

    CONTEXT:
    {context_text}

    METADATA (USE THESE FOR CITATIONS:
    {metadatas}
    """

    # 3. Send to Phi-3 via Ollama
    response = ollama.chat(
        model='phi3',
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': query}
        ]
    )

    return response['message']['content']

# --- THE DEMO LOOP ---
if __name__ == "__main__":
    print("--- ESRS AI Assistant Loaded ---")
    while True:
        user_input = input("\nAsk a question about ESRS (or type 'exit'): ")
        if user_input.lower() == 'exit':
            break
        
        answer = ask_esrs_assistant(user_input)
        print(f"\nAI ANSWER:\n{answer}")