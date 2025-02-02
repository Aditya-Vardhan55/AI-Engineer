import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from services.retrieval_service import retrieve_similar_queries, retrieve_from_pinecone

MODEL_PATH = "storage/fine_tuned_model"
model = AutoModelForCausalLM.from_pretrained(MODEL_PATH)
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

def generate_ai_response(query: str):
    """ 
    Generates an AI response based on the query and past interactions.
    """
    
    # Retrieve similar queries
    similar_queries = retrieve_similar_queries(query)
    similar_pinecone_queries = retrieve_from_pinecone(query)
    
    # Prepare prompt with context
    context = "\n".join(similar_queries + similar_pinecone_queries)
    prompt = f"User: {query}\n\nPast Interactions:\n{context}\n\nAI:"
    
    # Tokenize input
    inputs = tokenizer(prompt, return_tensors="pt", truncation= True, max_length= 512)
    
    # Generate response
    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens= 100, temperature= 0.7)
        
    response = tokenizer.decode(output[0], skip_special_tokens= True)
    return response
    