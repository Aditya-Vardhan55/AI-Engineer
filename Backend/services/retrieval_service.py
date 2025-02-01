import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session
from models.interaction_model import Interaction
import pinecone

# Load sentence embedding model
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Initialize FAISS index
faiss_index = faiss.IndexFlatL2(384)    # 384 dimensions for MiniLM model
stored_queries = []

# Pinecone setup(if using Pinecone instead of FAISS)
PINECONE_API_KEY = "pcsk_2SVWTL_25RPpuV2nxGJEYd9YzFKbkH86BWW2LG6MA5pAo4u66kwFnmsqMqLwSkwcjcYF8J"
PINECONE_ENV = "us-west1-gcp"
pinecone.init(api_key= PINECONE_API_KEY, environment= PINECONE_ENV)
pinecone_index = pinecone.Index("ai-engineer")

def store_query_embedding(db: Session, query: str, response: str):
    # Convert query to vector
    vector = embedding_model.encode(query).astype(np.float32)
    
    # Store in FAISS
    faiss_index.add(np.array([vector]))
    stored_queries.append(query)
    
    # Store in Pinecone (if needed)
    pinecone_index.upsert(vectors=[(query, vector.tolist())])
    
    # Store in DB
    interaction = Interaction(user_query= query, ai_response= response)
    db.add(interaction)
    db.commit()
    return interaction.id

def retrieve_similar_queries(query: str, top_k= 3):
    vector = embedding_model.encode(query).astype(np.float32)
    
    if faiss_index.ntotal > 0:
        _, indices = faiss_index.search(np.array([vector]), top_k)
        results = [stored_queries[i] for i in indices[0] if i < len(stored_queries)]
        return results
    
    return []

def retrieve_from_pinecone(query: str, top_k= 3):
    vector = embedding_model.encode(query).tolist()
    results = pinecone_index.query(vector, top_k= top_k, include_metadata= True)
    return [match["id"] for match in results["matches"]]