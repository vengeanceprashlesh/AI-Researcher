"""
AI Research Collaborator - Main Application
Multi-agent system for conducting academic research with memory and session management.

Author: Kaggle Agents Intensive Capstone Project
Track: Agents for Good (Education)
"""

import os
import json
from agents import OrchestratorAgent
from memory_manager import ResearchMemoryManager


def print_banner():
    """Print application banner."""
    print("\n" + "="*70)
    print("  AI RESEARCH COLLABORATOR")
    print("  Multi-Agent Research Assistant for Education")
    print("="*70 + "\n")


def print_results_summary(results: dict):
    """
    Print a summary of research results.
    
    Args:
        results: Research results dictionary
    """
    print("\n" + "="*70)
    print(" RESEARCH RESULTS SUMMARY")
    print("="*70)
    
    if "summary" in results:
        print("\n Summary:")
        print("-" * 70)
        print(results["summary"]["summary"][:500] + "..." if len(results["summary"]["summary"]) > 500 else results["summary"]["summary"])
    
    if "validation" in results:
        print("\n✓ Validation Report:")
        print("-" * 70)
        print(results["validation"]["validation_report"][:300] + "..." if len(results["validation"]["validation_report"]) > 300 else results["validation"]["validation_report"])
    
    if "report" in results:
        print(f"\n✍️ Full Report Generated: {results['report']['word_count']} words")
        print("-" * 70)
    
    print("\n" + "="*70)


def save_report_to_file(results: dict, topic: str, output_dir: str = "outputs"):
    """
    Save research report to a file.
    
    Args:
        results: Research results dictionary
        topic: Research topic
        output_dir: Output directory path
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create safe filename
    safe_topic = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in topic)
    safe_topic = safe_topic.replace(' ', '_')[:50]
    
    # Save full report if available
    if "report" in results:
        filename = os.path.join(output_dir, f"{safe_topic}_report.txt")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"AI Research Collaborator - Research Report\n")
            f.write(f"Topic: {topic}\n")
            f.write("="*70 + "\n\n")
            f.write(results["report"]["report"])
        print(f"\n Report saved to: {filename}")
    
    # Save JSON results
    json_filename = os.path.join(output_dir, f"{safe_topic}_results.json")
    with open(json_filename, 'w', encoding='utf-8') as f:
        # Create a simplified version for JSON
        json_results = {
            "topic": topic,
            "summary": results.get("summary", {}).get("summary", ""),
            "validation": results.get("validation", {}).get("validation_report", ""),
            "word_count": results.get("report", {}).get("word_count", 0)
        }
        json.dump(json_results, f, indent=2, ensure_ascii=False)
    print(f" Results saved to: {json_filename}")


def example_quick_research():
    """Example: Quick research on a topic."""
    print_banner()
    print(" Example 1: Quick Research\n")
    
    # Initialize memory manager and orchestrator
    memory_manager = ResearchMemoryManager()
    session_id = memory_manager.start_research_session("quick_research_demo")
    
    orchestrator = OrchestratorAgent()
    
    # Conduct quick research
    topic = "Impact of AI on education"
    print(f"Researching: {topic}\n")
    
    summary = orchestrator.quick_research(topic)
    
    print("\n Quick Summary:")
    print("-" * 70)
    print(summary)
    print("-" * 70)
    
    # Save to memory
    results = orchestrator.get_current_state()
    memory_manager.save_research_to_session(topic, results)
    
    # End session
    memory_manager.end_research_session()


def example_deep_research():
    """Example: Deep research with validation and report generation."""
    print_banner()
    print(" Example 2: Deep Research with Validation\n")
    
    # Initialize memory manager and orchestrator
    memory_manager = ResearchMemoryManager()
    session_id = memory_manager.start_research_session("deep_research_demo")
    
    orchestrator = OrchestratorAgent()
    
    # Conduct deep research
    topic = "Machine Learning in Personalized Education"
    print(f"Researching: {topic}\n")
    
    results = orchestrator.deep_research(topic)
    
    # Print summary
    print_results_summary(results)
    
    # Save to memory and file
    memory_manager.save_research_to_session(topic, results)
    save_report_to_file(results, topic)
    
    # Show memory context
    context = memory_manager.get_research_context()
    print(f"\n Memory Statistics:")
    print(f"   Total sessions: {context['statistics']['total_research_sessions']}")
    print(f"   Unique topics: {context['statistics']['unique_topics']}")
    
    # End session
    memory_manager.end_research_session()


def example_comparative_research():
    """Example: Compare multiple topics."""
    print_banner()
    print(" Example 3: Comparative Research\n")
    
    # Initialize memory manager and orchestrator
    memory_manager = ResearchMemoryManager()
    session_id = memory_manager.start_research_session("comparative_research_demo")
    
    orchestrator = OrchestratorAgent()
    
    # Compare topics
    topics = [
        "Online Learning Effectiveness",
        "Traditional Classroom Learning Effectiveness"
    ]
    
    results = orchestrator.research_and_compare(topics)
    
    print("\n Comparison Synthesis:")
    print("-" * 70)
    print(results["comparison"]["synthesis"])
    print("-" * 70)
    
    # Save to memory
    memory_manager.save_research_to_session(" vs ".join(topics), results)
    
    # End session
    memory_manager.end_research_session()


def example_custom_workflow():
    """Example: Custom research workflow."""
    print_banner()
    print(" Example 4: Custom Workflow\n")
    
    orchestrator = OrchestratorAgent()
    
    # Custom workflow: search → summarize → validate
    topic = "Gamification in Education"
    workflow = ["search", "summarize", "validate"]
    
    results = orchestrator.custom_workflow(topic, workflow)
    
    print("\n Custom Workflow Complete!")
    print(f"Executed steps: {', '.join(workflow)}")


def example_memory_retrieval():
    """Example: Retrieve previous research from memory."""
    print_banner()
    print(" Example 5: Memory Retrieval\n")
    
    memory_manager = ResearchMemoryManager()
    
    # Get research history
    history = memory_manager.memory_bank.get_history(limit=5)
    
    print(" Recent Research History:")
    print("-" * 70)
    for i, entry in enumerate(history, 1):
        print(f"{i}. {entry['topic']} - {entry['timestamp']}")
        if entry.get('has_report'):
            print("   ✍️ Full report available")
    
    print("\n" + "-" * 70)
    
    # Get statistics
    stats = memory_manager.memory_bank.get_statistics()
    print(f"\n Memory Bank Statistics:")
    print(f"   Total research sessions: {stats['total_research_sessions']}")
    print(f"   Unique topics: {stats['unique_topics']}")
    if stats['most_researched']:
        print(f"   Most researched: {stats['most_researched']}")


def interactive_mode():
    """Interactive research mode."""
    print_banner()
    print(" Interactive Research Mode")
    print("Enter a research topic or 'quit' to exit\n")
    
    memory_manager = ResearchMemoryManager()
    orchestrator = OrchestratorAgent()
    
    session_id = memory_manager.start_research_session("interactive_session")
    
    while True:
        topic = input("\n Research Topic: ").strip()
        
        if topic.lower() in ['quit', 'exit', 'q']:
            break
        
        if not topic:
            continue
        
        # Check if topic was researched before
        previous = memory_manager.retrieve_previous_research(topic)
        if previous:
            print(f"\n Found previous research on this topic!")
            use_previous = input("Use previous results? (y/n): ").strip().lower()
            if use_previous == 'y':
                print_results_summary(previous)
                continue
        
        # Conduct research
        depth = input("Research depth (quick/medium/deep) [medium]: ").strip() or "medium"
        
        results = orchestrator.conduct_research(
            topic,
            depth=depth,
            validate=(depth in ["medium", "deep"]),
            generate_report=(depth == "deep")
        )
        
        # Save results
        memory_manager.save_research_to_session(topic, results)
        
        # Ask if user wants to save report
        if "report" in results:
            save = input("\n Save report to file? (y/n): ").strip().lower()
            if save == 'y':
                save_report_to_file(results, topic)
    
    memory_manager.end_research_session()
    print("\n Thank you for using AI Research Collaborator!")


def main():
    """Main application entry point."""
    print_banner()
    print("Choose a demo mode:\n")
    print("1. Quick Research")
    print("2. Deep Research with Validation")
    print("3. Comparative Research")
    print("4. Custom Workflow")
    print("5. Memory Retrieval")
    print("6. Interactive Mode")
    print("0. Run All Examples")
    
    choice = input("\nEnter choice (0-6): ").strip()
    
    if choice == "1":
        example_quick_research()
    elif choice == "2":
        example_deep_research()
    elif choice == "3":
        example_comparative_research()
    elif choice == "4":
        example_custom_workflow()
    elif choice == "5":
        example_memory_retrieval()
    elif choice == "6":
        interactive_mode()
    elif choice == "0":
        example_quick_research()
        example_deep_research()
        example_comparative_research()
        example_custom_workflow()
        example_memory_retrieval()
    else:
        print("Invalid choice. Running deep research example...")
        example_deep_research()


if __name__ == "__main__":
    # Check for API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️  Warning: GOOGLE_API_KEY environment variable not set!")
        print("Please set your API key:")
        print("  export GOOGLE_API_KEY='your-api-key-here'  # Linux/Mac")
        print("  $env:GOOGLE_API_KEY='your-api-key-here'   # Windows PowerShell")
        print()
    
    main()
