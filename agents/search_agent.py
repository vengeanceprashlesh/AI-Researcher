"""
Literature Search Agent
Searches for research papers, articles, and academic content using Google Search tool.
"""

from google import genai
from google.genai import types
import os


class LiteratureSearchAgent:
    """Agent responsible for finding relevant research papers and articles."""
    
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        """
        Initialize the Literature Search Agent.
        
        Args:
            model_name: The Gemini model to use for this agent
        """
        self.client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
        self.model_name = model_name
        
        # System instruction for the search agent
        self.system_instruction = """
        You are a Literature Search Agent specialized in finding academic papers, 
        research articles, and credible sources on any given topic.
        
        Your role:
        1. Search for relevant papers, articles, and sources
        2. Identify the most credible and recent sources
        3. Extract key information: titles, authors, publication dates, URLs
        4. Prioritize peer-reviewed content and authoritative sources
        5. Return results in a structured format
        
        Always use the Google Search tool to find information.
        """
    
    def search(self, topic: str, num_sources: int = 5) -> dict:
        """
        Search for literature on a given topic.
        
        Args:
            topic: The research topic to search for
            num_sources: Number of sources to find
            
        Returns:
            Dictionary containing search results with sources
        """
        prompt = f"""
        Search for academic papers and credible articles about: {topic}
        
        Find {num_sources} high-quality sources. For each source, extract:
        - Title
        - Author(s) if available
        - Publication date
        - URL
        - Brief summary of relevance
        
        Focus on recent publications (last 5 years) and peer-reviewed content.
        """
        
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                temperature=0.4,
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
        
        return {
            "topic": topic,
            "search_results": response.text,
            "num_sources": num_sources
        }
    
    def targeted_search(self, query: str) -> str:
        """
        Perform a targeted search for specific information.
        
        Args:
            query: Specific search query
            
        Returns:
            Search results as text
        """
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=query,
            config=types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                temperature=0.3,
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
        
        return response.text
