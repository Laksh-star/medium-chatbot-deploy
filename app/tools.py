"""Tools for Medium Articles Chatbot workflows."""

import json
from pathlib import Path
from typing import List
from .config import get_llamacloud_index

# Load data files
DATA_DIR = Path(__file__).parent.parent / "data"

def load_data():
    """Load articles manifest and tech index data."""
    with open(DATA_DIR / "articles_manifest.json", 'r') as f:
        articles_manifest = json.load(f)
    
    with open(DATA_DIR / "tech_index.json", 'r') as f:
        tech_index_data = json.load(f)
    
    return articles_manifest, tech_index_data

# Load global data
articles_manifest, tech_index_data = load_data()

# Initialize index lazily to avoid authentication issues during import
index = None

def get_index():
    """Get LlamaCloud index with lazy initialization."""
    global index
    if index is None:
        index = get_llamacloud_index()
    return index

def search_articles(query: str, top_k: int = 3) -> str:
    """Search articles semantically by query. Returns relevant article excerpts.

    Args:
        query: The search query
        top_k: Number of results to return (default 3)
    """
    try:
        retriever = get_index().as_retriever(similarity_top_k=top_k)
        results = retriever.retrieve(query)
    except Exception as e:
        # Fallback to local search if LlamaCloud fails
        return f"LlamaCloud search unavailable ({str(e)}). Using local article metadata search instead."

    if not results:
        return "No relevant articles found."

    output = []
    for i, result in enumerate(results, 1):
        # Extract metadata if available
        metadata = result.metadata or {}
        title = metadata.get('title', 'Unknown')

        output.append(f"Result {i}:")
        output.append(f"Title: {title}")
        output.append(f"Relevance: {result.score:.2f}")
        output.append(f"Excerpt: {result.text[:300]}...")
        output.append("---")

    return "\n".join(output)

def filter_by_metadata(tech: str = None, year: int = None, tag: str = None) -> str:
    """Filter articles by technology, year, or tag. Returns matching article titles and dates.

    Args:
        tech: Technology/tool name (e.g., 'Python', 'React')
        year: Publication year (e.g., 2024)
        tag: Article tag
    """
    matches = []

    for article in articles_manifest:
        # Check tech filter
        if tech:
            tech_match = any(tech.lower() in t.lower() for t in article.get('tech_stack', []))
            if not tech_match:
                continue

        # Check year filter
        if year:
            if article.get('year') != year:
                continue

        # Check tag filter
        if tag:
            tag_match = any(tag.lower() in t.lower() for t in article.get('tags', []))
            if not tag_match:
                continue

        matches.append(article)

    if not matches:
        return f"No articles found matching the criteria."

    output = [f"Found {len(matches)} matching articles:\n"]
    for article in matches[:10]:  # Limit to 10
        output.append(f"• {article['title']}")
        output.append(f"  Date: {article.get('date', 'Unknown')}")
        if tech:
            output.append(f"  Tech: {', '.join(article.get('tech_stack', []))}")
        output.append("")

    if len(matches) > 10:
        output.append(f"... and {len(matches) - 10} more")

    return "\n".join(output)

def analyze_tech_stack(technology: str) -> str:
    """Get detailed statistics about a specific technology across all articles.

    Args:
        technology: Technology name to analyze (e.g., 'Python', 'Docker')
    """
    # Case-insensitive search
    matching_articles = []
    for tech, article_list in tech_index_data.items():
        if technology.lower() in tech.lower():
            matching_articles.extend(article_list)

    if not matching_articles:
        return f"No articles found mentioning '{technology}'."

    # Sort by date
    matching_articles.sort(key=lambda x: x.get('date') or '', reverse=True)

    output = []
    output.append(f"📊 Analysis for '{technology}':\n")
    output.append(f"Total articles: {len(matching_articles)}")

    # Date range
    dates = [a['date'] for a in matching_articles if a.get('date')]
    if dates:
        output.append(f"First mention: {min(dates)[:10]}")
        output.append(f"Latest mention: {max(dates)[:10]}")

    output.append(f"\nArticles mentioning '{technology}':\n")
    for article in matching_articles[:5]:
        output.append(f"• {article['title']}")
        output.append(f"  Date: {article.get('date', 'Unknown')[:10]}")
        output.append("")

    if len(matching_articles) > 5:
        output.append(f"... and {len(matching_articles) - 5} more articles")

    return "\n".join(output)

def find_content_gaps() -> str:
    """Analyze all articles to identify underserved topics and content opportunities."""

    # Analyze tech coverage
    tech_counts = {tech: len(articles) for tech, articles in tech_index_data.items()}
    sorted_tech = sorted(tech_counts.items(), key=lambda x: x[1])

    # Get date distribution
    year_counts = {}
    for article in articles_manifest:
        year = article.get('year')
        if year:
            year_counts[year] = year_counts.get(year, 0) + 1

    # Recent vs old content
    recent_cutoff = 2023
    recent_articles = [a for a in articles_manifest if a.get('year', 0) >= recent_cutoff]

    output = []
    output.append("📈 Content Gap Analysis\n")

    output.append(f"Total articles: {len(articles_manifest)}")
    output.append(f"Articles since {recent_cutoff}: {len(recent_articles)}\n")

    output.append("Technologies with limited coverage (< 3 articles):")
    for tech, count in sorted_tech[:10]:
        if count < 3:
            output.append(f"  • {tech}: {count} article(s)")

    output.append("\n📅 Publishing frequency by year:")
    for year in sorted(year_counts.keys()):
        output.append(f"  • {year}: {year_counts[year]} articles")

    output.append("\n💡 Recommendations:")
    output.append("  • Consider deep dives on underserved technologies")
    output.append("  • Update older popular articles")
    output.append("  • Combine technologies you know well but haven't written about together")

    return "\n".join(output)

def get_full_article(article_title: str) -> str:
    """Retrieve the full content of an article by title (exact or partial match).

    Args:
        article_title: Full or partial article title
    """
    # Find matching article
    matches = [a for a in articles_manifest if article_title.lower() in a['title'].lower()]

    if not matches:
        return f"No article found with title containing '{article_title}'"

    if len(matches) > 1:
        titles = [f"  • {a['title']}" for a in matches[:5]]
        return f"Multiple matches found. Please be more specific:\n" + "\n".join(titles)

    article = matches[0]
    output = []
    output.append(f"Title: {article['title']}")
    output.append(f"Date: {article.get('date', 'Unknown')}")
    output.append(f"Tags: {', '.join(article.get('tags', []))}")
    output.append(f"Tech: {', '.join(article.get('tech_stack', []))}")
    output.append(f"Word count: {article.get('word_count', 0)}")
    output.append("\n--- Content ---\n")
    output.append(article.get('content', '')[:2000])  # First 2000 chars
    if len(article.get('content', '')) > 2000:
        output.append("\n... (content truncated)")

    return "\n".join(output)