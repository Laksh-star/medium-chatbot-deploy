# Medium Articles Chatbot - LlamaCloud Deployment

AI-powered chatbot for exploring and analyzing Medium articles with three specialized modes.

## Architecture

- **Discovery Workflow**: Public article discovery with summaries
- **Tech Explorer Workflow**: Technical expertise showcase  
- **Analytics Workflow**: Private content analytics and strategy recommendations

## Quick Start

### 1. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API keys
LLAMA_CLOUD_API_KEY=llx-your-key
OPENAI_API_KEY=sk-your-key
```

### 2. Local Development

```bash
# Install dependencies
pip install llama-deploy

# Start local development server
llamactl serve

# Access workflows at:
# http://localhost:4501/deployments/discovery
# http://localhost:4501/deployments/tech-explorer  
# http://localhost:4501/deployments/analytics
```

### 3. Cloud Deployment

```bash
# Initialize git repository
git init
git add -A
git commit -m "Initial Medium chatbot deployment"
git remote add origin <your-repo-url>
git push -u origin main

# Deploy to LlamaCloud
llamactl deployments create
```

## API Usage

### Discovery Workflow
```python
import requests

response = requests.post(
    "https://api.cloud.llamaindex.ai/deployments/medium-discovery/run",
    headers={"Authorization": "Bearer <token>"},
    json={"query": "What Python articles do you have?"}
)
```

### Tech Explorer Workflow
```python
response = requests.post(
    "https://api.cloud.llamaindex.ai/deployments/medium-tech-explorer/run",
    headers={"Authorization": "Bearer <token>"},
    json={"query": "Show me the author's AI expertise"}
)
```

### Analytics Workflow
```python
response = requests.post(
    "https://api.cloud.llamaindex.ai/deployments/medium-analytics/run", 
    headers={"Authorization": "Bearer <token>"},
    json={"query": "What content gaps should I address?"}
)
```

## Project Structure

```
medium-chatbot-deploy/
├── app/
│   ├── __init__.py
│   ├── config.py          # LlamaCloud and API configuration
│   ├── tools.py           # Search and analysis tools
│   └── workflows.py       # Three workflow implementations
├── data/
│   ├── articles_manifest.json  # Article metadata and content
│   └── tech_index.json         # Technology to articles mapping
├── pyproject.toml         # Project configuration and dependencies
├── deployment.yml         # LlamaDeploy configuration
└── README.md             # This file
```

## Workflows

### 1. Discovery Workflow
- **Purpose**: Public article discovery
- **Features**: Semantic search, technology filtering, brief summaries
- **Tools**: `search_articles`, `filter_by_metadata`, `analyze_tech_stack`

### 2. Tech Explorer Workflow  
- **Purpose**: Technical expertise showcase
- **Features**: Technology analysis, skill demonstration, timeline evolution
- **Tools**: `search_articles`, `filter_by_metadata`, `analyze_tech_stack`

### 3. Analytics Workflow
- **Purpose**: Private content analytics
- **Features**: Content gaps, strategy recommendations, full article access
- **Tools**: All tools including `find_content_gaps`, `get_full_article`

## Data Sources

- **Articles**: 300+ processed Medium articles with metadata
- **Technologies**: Automatically extracted tech stack from articles
- **LlamaCloud Index**: Semantic search across all content

## Environment Variables

- `LLAMA_CLOUD_API_KEY`: Required for LlamaCloud access
- `OPENAI_API_KEY`: Required for LLM and embeddings
- `INDEX_NAME`: LlamaCloud index name (default: medium_articles_chatbot_new)
- `PROJECT_NAME`: LlamaCloud project (default: Default)
- `ORGANIZATION_ID`: Your LlamaCloud organization ID

## Development

### Testing Workflows Locally

```bash
# Test discovery workflow
curl -X POST http://localhost:4501/deployments/discovery/run \
  -H "Content-Type: application/json" \
  -d '{"query": "What are your AI articles about?"}'

# Test tech explorer workflow  
curl -X POST http://localhost:4501/deployments/tech-explorer/run \
  -H "Content-Type: application/json" \
  -d '{"query": "What technologies does the author use?"}'

# Test analytics workflow
curl -X POST http://localhost:4501/deployments/analytics/run \
  -H "Content-Type: application/json" \
  -d '{"query": "What content gaps should I address?"}'
```

### Updating Deployment

```bash
# Update code
git add -A
git commit -m "Update workflows"
git push

# Redeploy
llamactl deployments update
```

## Troubleshooting

- **API Key Issues**: Verify `.env` file and environment variables
- **Index Connection**: Check LlamaCloud index status and configuration
- **Workflow Errors**: Review logs with `llamactl logs`
- **Deployment Issues**: Ensure git repository is properly configured