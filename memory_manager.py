"""
Memory Management System
Implements session management and memory bank for context persistence.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional


class MemoryBank:
    """
    Long-term memory storage for research context and findings.
    
    Stores and retrieves research history across sessions.
    """
    
    def __init__(self, storage_path: str = "memory_bank.json"):
        """
        Initialize the Memory Bank.
        
        Args:
            storage_path: Path to the memory storage file
        """
        self.storage_path = storage_path
        self.memory = self._load_memory()
    
    def _load_memory(self) -> Dict[str, Any]:
        """Load memory from storage file."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load memory bank: {e}")
                return {"research_history": [], "topics": {}}
        return {"research_history": [], "topics": {}}
    
    def _save_memory(self):
        """Save memory to storage file."""
        try:
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save memory bank: {e}")
    
    def store_research(self, topic: str, results: Dict[str, Any]):
        """
        Store research results in long-term memory.
        
        Args:
            topic: Research topic
            results: Research results dictionary
        """
        entry = {
            "topic": topic,
            "timestamp": datetime.now().isoformat(),
            "summary": results.get("summary", {}).get("summary", ""),
            "has_validation": "validation" in results,
            "has_report": "report" in results
        }
        
        # Add to research history
        self.memory["research_history"].append(entry)
        
        # Store detailed results by topic
        self.memory["topics"][topic] = {
            "last_researched": datetime.now().isoformat(),
            "results": results,
            "research_count": self.memory["topics"].get(topic, {}).get("research_count", 0) + 1
        }
        
        self._save_memory()
        print(f"💾 Stored research on '{topic}' in memory bank")
    
    def retrieve_research(self, topic: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve previous research on a topic.
        
        Args:
            topic: Topic to retrieve
            
        Returns:
            Previous research results or None
        """
        if topic in self.memory["topics"]:
            return self.memory["topics"][topic]["results"]
        return None
    
    def get_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent research history.
        
        Args:
            limit: Maximum number of entries to return
            
        Returns:
            List of recent research entries
        """
        return self.memory["research_history"][-limit:]
    
    def search_memory(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Search memory for topics containing keyword.
        
        Args:
            keyword: Keyword to search for
            
        Returns:
            List of matching entries
        """
        keyword_lower = keyword.lower()
        matches = []
        
        for entry in self.memory["research_history"]:
            if keyword_lower in entry["topic"].lower():
                matches.append(entry)
        
        return matches
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get memory bank statistics."""
        return {
            "total_research_sessions": len(self.memory["research_history"]),
            "unique_topics": len(self.memory["topics"]),
            "most_researched": max(
                self.memory["topics"].items(),
                key=lambda x: x[1]["research_count"],
                default=(None, {"research_count": 0})
            )[0] if self.memory["topics"] else None
        }
    
    def clear_memory(self):
        """Clear all memory."""
        self.memory = {"research_history": [], "topics": {}}
        self._save_memory()
        print("🗑️ Memory bank cleared")


class InMemorySessionService:
    """
    Session service for managing research sessions.
    
    Maintains state within a single session and coordinates with Memory Bank.
    """
    
    def __init__(self):
        """Initialize the session service."""
        self.sessions = {}
        self.current_session_id = None
    
    def create_session(self, session_id: str = None) -> str:
        """
        Create a new research session.
        
        Args:
            session_id: Optional session ID, generated if not provided
            
        Returns:
            Session ID
        """
        if session_id is None:
            session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.sessions[session_id] = {
            "id": session_id,
            "created_at": datetime.now().isoformat(),
            "state": {},
            "history": []
        }
        
        self.current_session_id = session_id
        print(f"📝 Created session: {session_id}")
        return session_id
    
    def get_session(self, session_id: str = None) -> Optional[Dict[str, Any]]:
        """
        Get a session by ID.
        
        Args:
            session_id: Session ID, uses current if not provided
            
        Returns:
            Session data or None
        """
        if session_id is None:
            session_id = self.current_session_id
        
        return self.sessions.get(session_id)
    
    def update_session_state(self, key: str, value: Any, session_id: str = None):
        """
        Update session state.
        
        Args:
            key: State key
            value: State value
            session_id: Session ID, uses current if not provided
        """
        if session_id is None:
            session_id = self.current_session_id
        
        if session_id and session_id in self.sessions:
            self.sessions[session_id]["state"][key] = value
            self.sessions[session_id]["history"].append({
                "timestamp": datetime.now().isoformat(),
                "action": f"Updated {key}"
            })
    
    def get_session_state(self, session_id: str = None) -> Dict[str, Any]:
        """
        Get session state.
        
        Args:
            session_id: Session ID, uses current if not provided
            
        Returns:
            Session state dictionary
        """
        if session_id is None:
            session_id = self.current_session_id
        
        if session_id and session_id in self.sessions:
            return self.sessions[session_id]["state"]
        
        return {}
    
    def end_session(self, session_id: str = None):
        """
        End a session.
        
        Args:
            session_id: Session ID, uses current if not provided
        """
        if session_id is None:
            session_id = self.current_session_id
        
        if session_id and session_id in self.sessions:
            self.sessions[session_id]["ended_at"] = datetime.now().isoformat()
            print(f"✅ Ended session: {session_id}")
            
            if session_id == self.current_session_id:
                self.current_session_id = None
    
    def list_sessions(self) -> List[str]:
        """List all session IDs."""
        return list(self.sessions.keys())
    
    def get_session_history(self, session_id: str = None) -> List[Dict[str, Any]]:
        """
        Get session history.
        
        Args:
            session_id: Session ID, uses current if not provided
            
        Returns:
            List of history entries
        """
        if session_id is None:
            session_id = self.current_session_id
        
        if session_id and session_id in self.sessions:
            return self.sessions[session_id]["history"]
        
        return []


class ResearchMemoryManager:
    """
    Unified memory manager combining session service and memory bank.
    """
    
    def __init__(self, storage_path: str = "memory_bank.json"):
        """
        Initialize the research memory manager.
        
        Args:
            storage_path: Path to memory bank storage
        """
        self.memory_bank = MemoryBank(storage_path)
        self.session_service = InMemorySessionService()
        self.current_session = None
    
    def start_research_session(self, session_name: str = None) -> str:
        """
        Start a new research session.
        
        Args:
            session_name: Optional session name
            
        Returns:
            Session ID
        """
        session_id = self.session_service.create_session(session_name)
        self.current_session = session_id
        return session_id
    
    def save_research_to_session(self, topic: str, results: Dict[str, Any]):
        """
        Save research results to current session and memory bank.
        
        Args:
            topic: Research topic
            results: Research results
        """
        # Save to session
        self.session_service.update_session_state("last_topic", topic)
        self.session_service.update_session_state("last_results", results)
        
        # Save to long-term memory
        self.memory_bank.store_research(topic, results)
    
    def retrieve_previous_research(self, topic: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve previous research from memory bank.
        
        Args:
            topic: Topic to retrieve
            
        Returns:
            Previous research or None
        """
        return self.memory_bank.retrieve_research(topic)
    
    def get_research_context(self) -> Dict[str, Any]:
        """
        Get current research context from session and memory.
        
        Returns:
            Research context dictionary
        """
        session_state = self.session_service.get_session_state()
        history = self.memory_bank.get_history(limit=5)
        
        return {
            "current_session": self.current_session,
            "session_state": session_state,
            "recent_history": history,
            "statistics": self.memory_bank.get_statistics()
        }
    
    def end_research_session(self):
        """End the current research session."""
        if self.current_session:
            self.session_service.end_session(self.current_session)
            self.current_session = None
