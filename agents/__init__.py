"""
AI Research Collaborator - Agents Module
Multi-agent system for conducting academic research.
"""

import os
from dotenv import load_dotenv

# Load environment variables from a local .env file if present
# This lets you keep GOOGLE_API_KEY in .env without hard-coding it.
load_dotenv()

from .search_agent import LiteratureSearchAgent
from .summarization_agent import SummarizationAgent
from .fact_checker_agent import FactCheckerAgent
from .writer_agent import WriterAgent
from .orchestrator_agent import OrchestratorAgent

__all__ = [
    "LiteratureSearchAgent",
    "SummarizationAgent",
    "FactCheckerAgent",
    "WriterAgent",
    "OrchestratorAgent"
]
