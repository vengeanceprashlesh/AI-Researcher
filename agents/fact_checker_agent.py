"""
Fact-Checker Agent
Validates claims and statements across multiple sources.
"""

from google import genai
from google.genai import types
import os


class FactCheckerAgent:
    """Agent responsible for fact-checking and validating claims."""
    
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        """
        Initialize the Fact-Checker Agent.
        
        Args:
            model_name: The Gemini model to use for this agent
        """
        self.client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
        self.model_name = model_name
        
        # System instruction for the fact-checker agent
        self.system_instruction = """
        You are a Fact-Checker Agent specialized in validating claims and 
        statements against multiple credible sources.
        
        Your role:
        1. Verify factual claims using Google Search
        2. Cross-reference information across multiple sources
        3. Identify supported vs. unsupported claims
        4. Rate confidence level of each claim
        5. Flag potentially misleading or controversial statements
        6. Provide evidence for your assessments
        
        Always be thorough, objective, and evidence-based in your fact-checking.
        """
    
    def check_claim(self, claim: str) -> dict:
        """
        Fact-check a specific claim.
        
        Args:
            claim: The claim to verify
            
        Returns:
            Dictionary containing verification results
        """
        prompt = f"""
        Fact-check this claim: "{claim}"
        
        Use Google Search to find evidence. Provide:
        1. Verification Status: TRUE / PARTIALLY TRUE / FALSE / UNVERIFIABLE
        2. Confidence Level: HIGH / MEDIUM / LOW
        3. Supporting Evidence (with sources)
        4. Contradicting Evidence (if any)
        5. Context or Nuances
        
        Be thorough and cite specific sources.
        """
        
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                temperature=0.2,
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
        
        return {
            "claim": claim,
            "verification": response.text
        }
    
    def validate_content(self, content: str, topic: str) -> dict:
        """
        Validate the accuracy of content about a topic.
        
        Args:
            content: Content to validate
            topic: The topic context
            
        Returns:
            Dictionary containing validation results
        """
        prompt = f"""
        Validate the following content about '{topic}':
        
        {content}
        
        Check for:
        1. Factual accuracy of key claims
        2. Outdated information
        3. Misleading statements
        4. Missing important context
        5. Overall reliability score (0-100)
        
        Use Google Search to verify claims. Provide detailed feedback.
        """
        
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                temperature=0.2,
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
        
        return {
            "content_validated": True,
            "topic": topic,
            "validation_report": response.text
        }
    
    def cross_reference(self, statements: list[str]) -> dict:
        """
        Cross-reference multiple statements for consistency.
        
        Args:
            statements: List of statements to cross-reference
            
        Returns:
            Dictionary containing cross-reference analysis
        """
        formatted_statements = "\n".join([f"{i+1}. {s}" for i, s in enumerate(statements)])
        
        prompt = f"""
        Cross-reference these statements for consistency and accuracy:
        
        {formatted_statements}
        
        Identify:
        1. Contradictions between statements
        2. Statements that support each other
        3. Which statements need verification
        4. Overall consistency score
        
        Use Google Search as needed to verify claims.
        """
        
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                temperature=0.2,
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
        
        return {
            "num_statements": len(statements),
            "cross_reference_report": response.text
        }
