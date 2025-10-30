"""Simple API using LlamaCloud index directly"""

import os
from fastapi import FastAPI
from pydantic import BaseModel
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_cloud_services import LlamaCloudIndex

# Initialize FastAPI
app = FastAPI(title="Medium Articles Chatbot API")

# Configuration
LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
INDEX_NAME = "medium_articles_chatbot_new"
PROJECT_NAME = "Default"
ORGANIZATION_ID = "ab776bbf-1681-49f8-9522-4d70edea9ef2"

# Configure settings
Settings.llm = OpenAI(model="gpt-4o-mini", temperature=0.7)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

# Initialize index
index = LlamaCloudIndex(
    name=INDEX_NAME,
    project_name=PROJECT_NAME,
    organization_id=ORGANIZATION_ID,
    api_key=LLAMA_CLOUD_API_KEY
)

class QueryRequest(BaseModel):
    query: str
    mode: str = "discovery"  # discovery, tech-explorer, analytics

@app.post("/chat")
async def chat(request: QueryRequest):
    """Chat with the Medium articles chatbot"""
    try:
        # Create query engine
        query_engine = index.as_query_engine()
        
        # Add mode-specific system prompt
        if request.mode == "discovery":
            prompt = f"You are a discovery agent. Provide brief summaries and teasers about articles. Query: {request.query}"
        elif request.mode == "tech-explorer":
            prompt = f"You are a tech explorer. Analyze technical expertise and technology patterns. Query: {request.query}"
        elif request.mode == "analytics":
            prompt = f"You are an analytics agent. Provide detailed content analysis and strategy recommendations. Query: {request.query}"
        else:
            prompt = request.query
            
        # Query the index
        response = query_engine.query(prompt)
        
        return {
            "response": str(response),
            "mode": request.mode,
            "status": "success"
        }
    except Exception as e:
        return {
            "error": str(e),
            "status": "error"
        }

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)