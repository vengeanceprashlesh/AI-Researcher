"""
Simple Demo Script
Quick test to verify the AI Research Collaborator is working.
"""

import os
from agents import OrchestratorAgent
from memory_manager import ResearchMemoryManager


def main():
    """Run a simple demo."""
    print("\n" + "="*70)
    print("🎓 AI RESEARCH COLLABORATOR - DEMO")
    print("="*70)
    
    # Check API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("\n⚠️  ERROR: GOOGLE_API_KEY environment variable not set!")
        print("\nPlease set your API key:")
        print("  Windows PowerShell:")
        print("    $env:GOOGLE_API_KEY='your-api-key-here'")
        print("\n  Linux/Mac:")
        print("    export GOOGLE_API_KEY='your-api-key-here'")
        return
    
    print("\n✅ API Key found!")
    print("\n🔬 Running Quick Research Demo...\n")
    
    try:
        # Initialize
        orchestrator = OrchestratorAgent()
        memory_manager = ResearchMemoryManager()
        
        # Start session
        session_id = memory_manager.start_research_session("demo_session")
        
        # Quick research
        topic = "Benefits of AI in Education"
        print(f"Topic: {topic}")
        print("-" * 70)
        
        results = orchestrator.conduct_research(
            topic=topic,
            depth="quick",
            validate=False,
            generate_report=False
        )
        
        # Display summary
        if "summary" in results:
            summary = results["summary"]["summary"]
            print("\n📝 Research Summary:")
            print("-" * 70)
            print(summary[:500] + "..." if len(summary) > 500 else summary)
            print("-" * 70)
        
        # Save to memory
        memory_manager.save_research_to_session(topic, results)
        
        # Show stats
        stats = memory_manager.memory_bank.get_statistics()
        print(f"\n📊 Memory Stats:")
        print(f"   Total sessions: {stats['total_research_sessions']}")
        print(f"   Unique topics: {stats['unique_topics']}")
        
        # End session
        memory_manager.end_research_session()
        
        print("\n" + "="*70)
        print("✅ DEMO COMPLETE!")
        print("="*70)
        print("\nNext steps:")
        print("  1. Run 'python main.py' for more examples")
        print("  2. Check README.md for full documentation")
        print("  3. Try interactive mode: python main.py (option 6)")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("  1. Verify API key is correct")
        print("  2. Check internet connection")
        print("  3. Ensure all dependencies are installed: pip install -r requirements.txt")


if __name__ == "__main__":
    main()
