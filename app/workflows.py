"""Medium Articles Chatbot Workflows for LlamaCloud deployment."""

from llama_index.core.workflow import Workflow, StartEvent, StopEvent, step
from .tools import (
    search_articles, 
    filter_by_metadata, 
    analyze_tech_stack, 
    find_content_gaps, 
    get_full_article
)

class DiscoveryWorkflow(Workflow):
    """Public Discovery Agent - helps users discover articles without revealing full content."""
    
    @step
    async def discover_articles(self, ev: StartEvent) -> StopEvent:
        """Process discovery queries with article search and filtering."""
        query = ev.get("query", "")
        
        if not query:
            return StopEvent(result="Please provide a question about the articles.")
        
        # Enhanced discovery logic with multiple search strategies
        result_parts = []
        
        # Try semantic search first
        search_results = search_articles(query, top_k=3)
        if "No relevant articles found" not in search_results:
            result_parts.append("🔍 **Search Results:**")
            result_parts.append(search_results)
        
        # Check if query mentions specific technologies
        tech_keywords = ["python", "ai", "claude", "openai", "llamaindex", "react", "docker"]
        mentioned_tech = [tech for tech in tech_keywords if tech.lower() in query.lower()]
        
        if mentioned_tech:
            for tech in mentioned_tech[:2]:  # Limit to 2 techs
                tech_analysis = analyze_tech_stack(tech)
                if "No articles found" not in tech_analysis:
                    result_parts.append(f"\n🔧 **{tech.title()} Coverage:**")
                    result_parts.append(tech_analysis)
        
        if not result_parts:
            result_parts = [
                "I couldn't find specific matches for your query. Here are some ways I can help:",
                "• Ask about specific technologies (Python, AI, LlamaIndex, etc.)",
                "• Request articles from specific years",
                "• Search for topics like 'patent filing', 'AI workflows', or 'productivity'"
            ]
        
        # Add discovery note
        result_parts.append("\n📚 **Note:** I provide article summaries and teasers to help you discover interesting content. For full articles, visit the original Medium posts.")
        
        return StopEvent(result="\n".join(result_parts))

class TechExplorerWorkflow(Workflow):
    """Tech Explorer Agent - showcases technical expertise and technology usage patterns."""
    
    @step
    async def explore_tech(self, ev: StartEvent) -> StopEvent:
        """Analyze and showcase technical expertise across articles."""
        query = ev.get("query", "")
        
        if not query:
            return StopEvent(result="Please ask about specific technologies or technical expertise.")
        
        result_parts = []
        result_parts.append("🔬 **Technical Expertise Analysis**\n")
        
        # Check for specific technology mentions
        if any(word in query.lower() for word in ["technology", "tech", "stack", "expertise"]):
            # Provide technology overview
            tech_summary = analyze_tech_stack("AI")  # Start with AI as main focus
            result_parts.append("**Primary Focus - AI Technologies:**")
            result_parts.append(tech_summary)
            
            # Add other key technologies
            other_techs = ["Python", "LlamaIndex", "Claude", "OpenAI"]
            for tech in other_techs:
                tech_analysis = analyze_tech_stack(tech)
                if "No articles found" not in tech_analysis:
                    result_parts.append(f"\n**{tech} Expertise:**")
                    result_parts.append(tech_analysis)
        
        # Technology-specific queries
        elif any(tech in query.lower() for tech in ["python", "ai", "claude", "openai", "llamaindex"]):
            # Extract mentioned technology
            for tech in ["python", "ai", "claude", "openai", "llamaindex"]:
                if tech in query.lower():
                    tech_analysis = analyze_tech_stack(tech)
                    result_parts.append(f"**{tech.title()} Expertise:**")
                    result_parts.append(tech_analysis)
                    break
        
        # Year-based evolution queries
        elif any(word in query.lower() for word in ["evolution", "timeline", "history", "over time"]):
            result_parts.append("**Technology Evolution Timeline:**")
            for year in [2023, 2024, 2025]:
                year_articles = filter_by_metadata(year=year)
                if "No articles found" not in year_articles:
                    result_parts.append(f"\n**{year}:**")
                    result_parts.append(year_articles[:500] + "..." if len(year_articles) > 500 else year_articles)
        
        # General search
        else:
            search_results = search_articles(query, top_k=3)
            result_parts.append("**Relevant Technical Content:**")
            result_parts.append(search_results)
        
        # Add expertise summary
        result_parts.append("\n💡 **Technical Profile:** Demonstrated expertise in AI technologies, automation tools, patent filing systems, and productivity workflows. Active exploration of cutting-edge AI platforms and their practical applications.")
        
        return StopEvent(result="\n".join(result_parts))

class AnalyticsWorkflow(Workflow):
    """Private Analytics Agent - provides deep insights and analytics for content strategy."""
    
    @step
    async def analyze_content(self, ev: StartEvent) -> StopEvent:
        """Perform comprehensive content analysis and strategy recommendations."""
        query = ev.get("query", "")
        
        if not query:
            return StopEvent(result="Please specify what type of analysis you'd like: content gaps, writing patterns, article performance, or strategy recommendations.")
        
        result_parts = []
        result_parts.append("📊 **Content Analytics Dashboard**\n")
        
        # Content gap analysis
        if any(word in query.lower() for word in ["gap", "opportunity", "missing", "underserved"]):
            gaps_analysis = find_content_gaps()
            result_parts.append("**Content Gap Analysis:**")
            result_parts.append(gaps_analysis)
        
        # Article retrieval for detailed analysis
        elif any(word in query.lower() for word in ["article", "content", "full", "detail"]):
            # Try to extract article title from query
            search_results = search_articles(query, top_k=5)
            result_parts.append("**Article Search Results:**")
            result_parts.append(search_results)
            
            # Offer to get full article if specific title is mentioned
            result_parts.append("\n💡 **Tip:** To get full article content, ask for a specific article title.")
        
        # Performance and patterns analysis
        elif any(word in query.lower() for word in ["pattern", "performance", "trend", "frequency"]):
            result_parts.append("**Writing Patterns Analysis:**")
            
            # Analyze publishing frequency
            frequency_analysis = filter_by_metadata()  # Get all articles
            result_parts.append(frequency_analysis[:1000])  # Truncate for display
            
            # Add content gaps for recommendations
            gaps = find_content_gaps()
            result_parts.append("\n**Strategic Recommendations:**")
            result_parts.append(gaps)
        
        # Technology focus analysis
        elif any(word in query.lower() for word in ["technology", "tech", "focus", "expertise"]):
            result_parts.append("**Technology Focus Analysis:**")
            for tech in ["AI", "Claude", "Python", "LlamaIndex", "OpenAI"]:
                tech_analysis = analyze_tech_stack(tech)
                if "No articles found" not in tech_analysis:
                    result_parts.append(f"\n**{tech}:**")
                    result_parts.append(tech_analysis)
        
        # Strategy recommendations
        elif any(word in query.lower() for word in ["strategy", "next", "recommend", "suggest", "improve"]):
            gaps_analysis = find_content_gaps()
            result_parts.append("**Content Strategy Recommendations:**")
            result_parts.append(gaps_analysis)
            
            result_parts.append("\n**Additional Strategic Insights:**")
            result_parts.append("• Consider creating series on AI workflow automation")
            result_parts.append("• Expand Python + AI integration tutorials")
            result_parts.append("• Document more real-world AI implementation case studies")
            result_parts.append("• Create beginner-friendly guides for identified technologies")
        
        # General analytics
        else:
            # Provide comprehensive overview
            gaps = find_content_gaps()
            result_parts.append("**Comprehensive Content Overview:**")
            result_parts.append(gaps)
            
            search_results = search_articles(query, top_k=3)
            result_parts.append("\n**Query-Specific Results:**")
            result_parts.append(search_results)
        
        result_parts.append("\n🔒 **Private Mode:** Full analytics access with detailed content insights and strategic recommendations.")
        
        return StopEvent(result="\n".join(result_parts))

# Export workflow instances
discovery_workflow = DiscoveryWorkflow()
tech_explorer_workflow = TechExplorerWorkflow()
analytics_workflow = AnalyticsWorkflow()