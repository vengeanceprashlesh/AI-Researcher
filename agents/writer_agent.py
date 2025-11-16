"""
Writer Agent
Generates research reports and documents with proper citations.
"""

from google import genai
from google.genai import types
import os


class WriterAgent:
    """Agent responsible for writing research reports and documents."""
    
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        """
        Initialize the Writer Agent.
        
        Args:
            model_name: The Gemini model to use for this agent
        """
        self.client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
        self.model_name = model_name
        
        # System instruction for the writer agent
        self.system_instruction = """
        You are a Writer Agent specialized in creating high-quality research 
        reports and academic documents.
        
        Your role:
        1. Write clear, well-structured research reports
        2. Include proper citations and references
        3. Maintain academic tone and rigor
        4. Organize information logically
        5. Create engaging introductions and conclusions
        6. Use appropriate formatting and structure
        
        Always write in a clear, professional academic style with proper attribution.
        """
    
    def write_report(self, topic: str, research_data: dict, style: str = "academic") -> dict:
        """
        Write a complete research report.
        
        Args:
            topic: The research topic
            research_data: Dictionary containing research findings, summaries, etc.
            style: Writing style (academic, technical, accessible)
            
        Returns:
            Dictionary containing the written report
        """
        # Extract data from research_data
        findings = research_data.get("findings", "")
        sources = research_data.get("sources", "")
        synthesis = research_data.get("synthesis", "")
        
        prompt = f"""
        Write a comprehensive research report on: {topic}
        
        Style: {style}
        
        Use the following research materials:
        
        FINDINGS:
        {findings}
        
        SOURCES:
        {sources}
        
        SYNTHESIS:
        {synthesis}
        
        Structure the report with:
        1. Title
        2. Abstract (150-200 words)
        3. Introduction
        4. Literature Review
        5. Key Findings
        6. Discussion
        7. Conclusion
        8. References (properly formatted)
        
        Make it comprehensive, well-cited, and engaging.
        """
        
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                temperature=0.5
            )
        )
        
        return {
            "topic": topic,
            "report": response.text,
            "style": style,
            "word_count": len(response.text.split())
        }
    
    def write_section(self, section_type: str, content: str, context: str = "") -> str:
        """
        Write a specific section of a research document.
        
        Args:
            section_type: Type of section (introduction, methodology, conclusion, etc.)
            content: Content to base the section on
            context: Additional context
            
        Returns:
            Written section text
        """
        prompt = f"""
        Write a {section_type} section based on:
        
        {content}
        
        Additional context: {context}
        
        Make it well-structured, clear, and appropriate for an academic paper.
        """
        
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                temperature=0.5
            )
        )
        
        return response.text
    
    def create_summary(self, full_report: str, length: str = "medium") -> dict:
        """
        Create an executive summary of a report.
        
        Args:
            full_report: The complete report text
            length: short (100 words), medium (250 words), long (500 words)
            
        Returns:
            Dictionary containing the summary
        """
        word_targets = {
            "short": 100,
            "medium": 250,
            "long": 500
        }
        
        target_words = word_targets.get(length, 250)
        
        prompt = f"""
        Create an executive summary of approximately {target_words} words for:
        
        {full_report}
        
        The summary should:
        1. Capture the main findings
        2. Highlight key conclusions
        3. Be accessible to non-specialists
        4. Maintain accuracy
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
            "summary": response.text,
            "target_length": length,
            "target_words": target_words
        }
    
    def format_citations(self, sources: list[dict], style: str = "APA") -> str:
        """
        Format citations in a specific style.
        
        Args:
            sources: List of source dictionaries with title, author, date, url
            style: Citation style (APA, MLA, Chicago)
            
        Returns:
            Formatted citations string
        """
        sources_text = "\n".join([str(s) for s in sources])
        
        prompt = f"""
        Format these sources in {style} citation style:
        
        {sources_text}
        
        Provide a properly formatted reference list.
        """
        
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                temperature=0.1
            )
        )
        
        return response.text
