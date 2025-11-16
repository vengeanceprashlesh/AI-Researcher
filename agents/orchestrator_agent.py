"""
Orchestrator Agent
Main coordinator that manages the research workflow and delegates to specialized agents.
"""

import json
import os
from typing import Dict, Any
from google import genai
from google.genai import types

from .search_agent import LiteratureSearchAgent
from .summarization_agent import SummarizationAgent
from .fact_checker_agent import FactCheckerAgent
from .writer_agent import WriterAgent


class OrchestratorAgent:
    """
    Main orchestrator that coordinates the research workflow.
    
    This agent manages the multi-agent system by:
    1. Planning the research workflow
    2. Delegating tasks to specialized agents
    3. Managing data flow between agents
    4. Synthesizing final results
    """
    
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        """
        Initialize the Orchestrator Agent and all sub-agents.
        
        Args:
            model_name: The Gemini model to use
        """
        self.client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
        self.model_name = model_name
        
        # Initialize specialized agents
        self.search_agent = LiteratureSearchAgent(model_name)
        self.summarization_agent = SummarizationAgent(model_name)
        self.fact_checker_agent = FactCheckerAgent(model_name)
        self.writer_agent = WriterAgent(model_name)
        
        # Workflow state
        self.current_research = {}
        
        # System instruction
        self.system_instruction = """
        You are an Orchestrator Agent that coordinates a research workflow.
        
        Your role:
        1. Plan the research process
        2. Delegate tasks to specialized agents
        3. Ensure quality and accuracy
        4. Synthesize results into coherent output
        
        You have access to:
        - Literature Search Agent: finds papers and articles
        - Summarization Agent: analyzes and synthesizes content
        - Fact-Checker Agent: validates claims
        - Writer Agent: generates reports
        
        Always maintain high research standards.
        """
    
    def conduct_research(
        self, 
        topic: str, 
        depth: str = "medium",
        validate: bool = True,
        generate_report: bool = True
    ) -> Dict[str, Any]:
        """
        Conduct a complete research workflow.
        
        Args:
            topic: The research topic
            depth: Research depth (quick, medium, deep)
            validate: Whether to fact-check findings
            generate_report: Whether to generate a full report
            
        Returns:
            Dictionary containing research results
        """
        print(f"\n🔬 Starting research on: {topic}")
        print("=" * 60)
        
        # Step 1: Literature Search
        print("\n📚 Phase 1: Literature Search")
        num_sources = {"quick": 3, "medium": 5, "deep": 10}.get(depth, 5)
        search_results = self.search_agent.search(topic, num_sources)
        print(f"✓ Found {num_sources} sources")
        
        # Store search results
        self.current_research["search_results"] = search_results
        
        # Step 2: Summarization
        print("\n📝 Phase 2: Analyzing and Summarizing")
        summary = self.summarization_agent.summarize(
            search_results["search_results"],
            focus=topic
        )
        print("✓ Analysis complete")
        
        # Store summary
        self.current_research["summary"] = summary
        
        # Step 3: Fact-Checking (if enabled)
        if validate:
            print("\n✓ Phase 3: Fact-Checking")
            validation = self.fact_checker_agent.validate_content(
                summary["summary"],
                topic
            )
            print("✓ Validation complete")
            self.current_research["validation"] = validation
        
        # Step 4: Generate Report (if enabled)
        if generate_report:
            print("\n✍️ Phase 4: Writing Report")
            
            # Prepare research data for writer
            research_data = {
                "findings": summary["summary"],
                "sources": search_results["search_results"],
                "synthesis": summary["summary"]
            }
            
            if validate:
                research_data["validation"] = validation["validation_report"]
            
            report = self.writer_agent.write_report(
                topic,
                research_data,
                style="academic"
            )
            print(f"✓ Report complete ({report['word_count']} words)")
            self.current_research["report"] = report
        
        print("\n" + "=" * 60)
        print("✅ Research Complete!")
        
        return self.current_research
    
    def quick_research(self, topic: str) -> str:
        """
        Perform quick research and return a brief summary.
        
        Args:
            topic: The research topic
            
        Returns:
            Quick summary text
        """
        results = self.conduct_research(
            topic,
            depth="quick",
            validate=False,
            generate_report=False
        )
        
        return results["summary"]["summary"]
    
    def deep_research(self, topic: str) -> Dict[str, Any]:
        """
        Perform comprehensive research with full validation and reporting.
        
        Args:
            topic: The research topic
            
        Returns:
            Complete research results
        """
        return self.conduct_research(
            topic,
            depth="deep",
            validate=True,
            generate_report=True
        )
    
    def research_and_compare(self, topics: list[str]) -> Dict[str, Any]:
        """
        Research multiple topics and compare findings.
        
        Args:
            topics: List of research topics
            
        Returns:
            Comparative analysis
        """
        print(f"\n🔬 Comparative Research: {len(topics)} topics")
        print("=" * 60)
        
        all_results = {}
        summaries = []
        
        # Research each topic
        for i, topic in enumerate(topics, 1):
            print(f"\n📚 Researching topic {i}/{len(topics)}: {topic}")
            results = self.conduct_research(
                topic,
                depth="medium",
                validate=False,
                generate_report=False
            )
            all_results[topic] = results
            summaries.append(results["summary"]["summary"])
        
        # Synthesize comparison
        print("\n🔄 Synthesizing comparison...")
        comparison_topic = " vs ".join(topics)
        synthesis = self.summarization_agent.synthesize_multiple(
            summaries,
            comparison_topic
        )
        
        return {
            "topics": topics,
            "individual_results": all_results,
            "comparison": synthesis
        }
    
    def custom_workflow(
        self,
        topic: str,
        workflow_steps: list[str]
    ) -> Dict[str, Any]:
        """
        Execute a custom research workflow.
        
        Args:
            topic: Research topic
            workflow_steps: List of steps (search, summarize, validate, write)
            
        Returns:
            Results from custom workflow
        """
        results = {"topic": topic, "steps": {}}
        
        print(f"\n🔬 Custom Workflow: {topic}")
        print(f"Steps: {', '.join(workflow_steps)}")
        print("=" * 60)
        
        for step in workflow_steps:
            if step == "search":
                print("\n📚 Searching...")
                results["steps"]["search"] = self.search_agent.search(topic)
                
            elif step == "summarize":
                print("\n📝 Summarizing...")
                content = results["steps"].get("search", {}).get("search_results", "")
                if content:
                    results["steps"]["summarize"] = self.summarization_agent.summarize(content)
                    
            elif step == "validate":
                print("\n✓ Validating...")
                content = results["steps"].get("summarize", {}).get("summary", "")
                if content:
                    results["steps"]["validate"] = self.fact_checker_agent.validate_content(
                        content, topic
                    )
                    
            elif step == "write":
                print("\n✍️ Writing...")
                research_data = {
                    "findings": results["steps"].get("summarize", {}).get("summary", ""),
                    "sources": results["steps"].get("search", {}).get("search_results", ""),
                    "synthesis": results["steps"].get("summarize", {}).get("summary", "")
                }
                results["steps"]["write"] = self.writer_agent.write_report(
                    topic, research_data
                )
        
        print("\n✅ Custom workflow complete!")
        return results
    
    def get_current_state(self) -> Dict[str, Any]:
        """Get the current research state."""
        return self.current_research
    
    def reset_state(self):
        """Reset the research state."""
        self.current_research = {}
        print("🔄 Research state reset")
