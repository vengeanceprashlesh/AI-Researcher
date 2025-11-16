"""
Summarization Agent
Analyzes and synthesizes research findings from multiple sources.
"""

from google import genai
from google.genai import types
import os


class SummarizationAgent:
    """Agent responsible for analyzing and summarizing research content."""
    
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        """
        Initialize the Summarization Agent.
        
        Args:
            model_name: The Gemini model to use for this agent
        """
        self.client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
        self.model_name = model_name
        
        # System instruction for the summarization agent
        self.system_instruction = """
        You are a Summarization Agent specialized in analyzing and synthesizing 
        research content from multiple sources.
        
        Your role:
        1. Read and understand complex research material
        2. Extract key findings and insights
        3. Identify common themes and patterns across sources
        4. Synthesize information into coherent summaries
        5. Maintain academic rigor and accuracy
        6. Highlight contradictions or debates in the literature
        
        Always be concise, accurate, and cite sources when possible.
        """
    
    def summarize(self, content: str, focus: str = None) -> dict:
        """
        Summarize research content.
        
        Args:
            content: The content to summarize
            focus: Optional focus area for the summary
            
        Returns:
            Dictionary containing the summary and key points
        """
        focus_instruction = f"\nFocus specifically on: {focus}" if focus else ""
        
        prompt = f"""
        Analyze and summarize the following research content:
        
        {content}
        {focus_instruction}
        
        Provide:
        1. Executive Summary (2-3 sentences)
        2. Key Findings (bullet points)
        3. Important Themes
        4. Notable Insights or Gaps
        """
        
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                temperature=0.3
            )
        )
        
        return {
            "summary": response.text,
            "source_length": len(content),
            "focus": focus
        }
    
    def synthesize_multiple(self, sources: list[str], topic: str) -> dict:
        """
        Synthesize information from multiple sources.
        
        Args:
            sources: List of source texts
            topic: The research topic
            
        Returns:
            Dictionary containing synthesized analysis
        """
        combined = "\n\n---SOURCE SEPARATOR---\n\n".join(sources)
        
        prompt = f"""
        Synthesize the following research sources about '{topic}':
        
        {combined}
        
        Provide a comprehensive synthesis that:
        1. Identifies consensus views
        2. Highlights disagreements or contradictions
        3. Notes emerging trends
        4. Summarizes the current state of knowledge
        5. Identifies research gaps
        """
        
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                temperature=0.4
            )
        )
        
        return {
            "synthesis": response.text,
            "num_sources": len(sources),
            "topic": topic
        }
