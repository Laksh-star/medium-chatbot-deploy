"""Configuration for Medium Articles Chatbot."""

import os
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_cloud_services import LlamaCloudIndex

# API Keys from environment
LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# LlamaCloud Index Configuration
INDEX_NAME = "medium_articles_chatbot_new"
PROJECT_NAME = "Default"
ORGANIZATION_ID = "ab776bbf-1681-49f8-9522-4d70edea9ef2"

# Configure LlamaIndex Settings
def configure_settings():
    """Configure global LlamaIndex settings."""
    Settings.llm = OpenAI(model="gpt-4o-mini", temperature=0.7)
    Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

def get_llamacloud_index():
    """Get configured LlamaCloud index."""
    configure_settings()
    
    return LlamaCloudIndex(
        name=INDEX_NAME,
        project_name=PROJECT_NAME,
        organization_id=ORGANIZATION_ID,
        api_key=LLAMA_CLOUD_API_KEY
    )