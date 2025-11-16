# 🏗️ Architecture Documentation

## System Architecture Overview

### High-Level Component View

```
┌──────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                           │
│                   (main.py / demo.py)                           │
└─────────────────────────┬────────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR AGENT                            │
│                  (orchestrator_agent.py)                        │
│                                                                  │
│  • Workflow Planning & Coordination                             │
│  • Task Delegation                                              │
│  • State Management                                             │
│  • Result Synthesis                                             │
└───┬──────────────┬──────────────┬──────────────┬────────────────┘
    │              │              │              │
    ▼              ▼              ▼              ▼
┌───────┐    ┌──────────┐   ┌──────────┐   ┌─────────┐
│SEARCH │    │SUMMARIZE │   │FACT-CHECK│   │ WRITER  │
│AGENT  │───▶│  AGENT   │──▶│  AGENT   │──▶│ AGENT   │
└───────┘    └──────────┘   └──────────┘   └─────────┘
    │              │              │              │
    │              │              │              │
    ▼              ▼              ▼              ▼
┌──────────────────────────────────────────────────────────────────┐
│                         TOOLS LAYER                              │
│                                                                  │
│  • Google Search API (Literature Search)                        │
│  • Google Search API (Fact Verification)                        │
│  • Code Execution (Optional)                                    │
└──────────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────────┐
│                    MEMORY & PERSISTENCE                          │
│                   (memory_manager.py)                           │
│                                                                  │
│  ┌────────────────────┐      ┌─────────────────────┐          │
│  │ Session Service    │      │   Memory Bank       │          │
│  │ (Short-term)       │◀────▶│   (Long-term)       │          │
│  │ • Active state     │      │ • Research history  │          │
│  │ • Workflow context │      │ • JSON persistence  │          │
│  └────────────────────┘      └─────────────────────┘          │
└──────────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────────┐
│                        GEMINI LLM                                │
│                  (gemini-2.0-flash-exp)                         │
└──────────────────────────────────────────────────────────────────┘
```

## Agent Workflow Sequence

### Standard Research Flow

```
1. USER REQUEST
   ↓
2. ORCHESTRATOR
   • Plans workflow
   • Sets depth (quick/medium/deep)
   ↓
3. SEARCH AGENT
   • Searches literature via Google
   • Finds N sources (3/5/10)
   • Extracts metadata
   ↓
4. SUMMARIZATION AGENT
   • Analyzes sources
   • Extracts key findings
   • Synthesizes information
   ↓
5. FACT-CHECKER AGENT (optional)
   • Validates claims
   • Cross-references sources
   • Provides confidence scores
   ↓
6. WRITER AGENT (optional)
   • Generates report
   • Formats citations
   • Creates structure
   ↓
7. MEMORY MANAGER
   • Saves to session
   • Stores in memory bank
   ↓
8. RESULT → USER
```

## Component Details

### 1. Orchestrator Agent

**File**: `agents/orchestrator_agent.py`

**Responsibilities**:
- Workflow coordination
- Agent delegation
- State management
- Result aggregation

**Key Methods**:
```python
conduct_research()     # Main workflow
quick_research()       # Fast path
deep_research()        # Full workflow
research_and_compare() # Multi-topic
custom_workflow()      # Custom steps
```

**Agent Type**: Sequential coordinator

---

### 2. Search Agent

**File**: `agents/search_agent.py`

**Responsibilities**:
- Literature discovery
- Source identification
- Metadata extraction

**Tools Used**:
- Google Search (built-in)

**Key Methods**:
```python
search()              # Main search
targeted_search()     # Specific query
```

**Temperature**: 0.4 (balanced)

---

### 3. Summarization Agent

**File**: `agents/summarization_agent.py`

**Responsibilities**:
- Content analysis
- Key finding extraction
- Multi-source synthesis

**Key Methods**:
```python
summarize()           # Single source
synthesize_multiple() # Multiple sources
```

**Temperature**: 0.3 (factual)

---

### 4. Fact-Checker Agent

**File**: `agents/fact_checker_agent.py`

**Responsibilities**:
- Claim verification
- Cross-referencing
- Confidence scoring

**Tools Used**:
- Google Search (verification)

**Key Methods**:
```python
check_claim()        # Single claim
validate_content()   # Full content
cross_reference()    # Multiple statements
```

**Temperature**: 0.2 (precise)

---

### 5. Writer Agent

**File**: `agents/writer_agent.py`

**Responsibilities**:
- Report generation
- Citation formatting
- Document structuring

**Key Methods**:
```python
write_report()       # Full report
write_section()      # Specific section
create_summary()     # Executive summary
format_citations()   # Citation formatting
```

**Temperature**: 0.5 (creative)

---

### 6. Memory Manager

**File**: `memory_manager.py`

**Components**:

#### Memory Bank (Long-term)
- Stores research history
- JSON file persistence
- Cross-session retrieval

**Methods**:
```python
store_research()     # Save research
retrieve_research()  # Get previous
get_history()        # Recent items
get_statistics()     # Usage stats
```

#### Session Service (Short-term)
- Active session state
- Workflow context
- In-memory storage

**Methods**:
```python
create_session()     # New session
update_session_state() # Update state
get_session_state()  # Read state
end_session()        # Close session
```

---

## Data Flow

### Research Data Structure

```json
{
  "search_results": {
    "topic": "string",
    "search_results": "string (formatted)",
    "num_sources": int
  },
  "summary": {
    "summary": "string",
    "source_length": int,
    "focus": "string"
  },
  "validation": {
    "content_validated": bool,
    "topic": "string",
    "validation_report": "string"
  },
  "report": {
    "topic": "string",
    "report": "string (full report)",
    "style": "string",
    "word_count": int
  }
}
```

## Configuration

**File**: `config/agent_config.py`

**Key Settings**:
```python
DEFAULT_MODEL = "gemini-2.0-flash-exp"
TEMPERATURE_SEARCH = 0.4
TEMPERATURE_SUMMARIZE = 0.3
TEMPERATURE_FACT_CHECK = 0.2
TEMPERATURE_WRITE = 0.5

QUICK_RESEARCH_SOURCES = 3
MEDIUM_RESEARCH_SOURCES = 5
DEEP_RESEARCH_SOURCES = 10
```

## Technology Stack

| Layer | Technology |
|-------|-----------|
| **LLM** | Google Gemini 2.0 Flash Exp |
| **Tools** | Google Search (built-in) |
| **Language** | Python 3.9+ |
| **Storage** | JSON (file-based) |
| **API** | Google GenAI SDK |

## Design Patterns

### 1. Multi-Agent Pattern
- Specialized agents for different tasks
- Clear separation of concerns
- Independent scalability

### 2. Orchestrator Pattern
- Central coordinator
- Workflow management
- State tracking

### 3. Repository Pattern
- Memory Bank as repository
- Abstract data access
- Persistent storage

### 4. Builder Pattern
- Flexible workflow construction
- Custom step composition

## Performance Characteristics

| Research Type | Agents Used | Time | Sources | Output |
|--------------|-------------|------|---------|--------|
| **Quick** | 2 (Search + Summarize) | ~5 min | 3 | Summary |
| **Medium** | 4 (+ Fact-check + Write) | ~10 min | 5 | Summary + Validation |
| **Deep** | 5 (All agents) | ~20 min | 10 | Full Report |

## Extension Points

### Adding New Agents
1. Create agent file in `agents/`
2. Inherit from base pattern
3. Define system instruction
4. Implement methods
5. Register in orchestrator

### Adding New Tools
1. Import from `google.genai.types`
2. Add to agent config
3. Use in agent methods

### Adding Workflows
1. Define in orchestrator
2. Specify agent sequence
3. Handle data flow

## Scalability Considerations

**Current**: Single-machine, sequential
**Future Options**:
- Parallel agent execution
- Distributed processing
- Cloud deployment (Agent Engine)
- Caching layer
- Database backend

## Security & Privacy

- No API keys in code
- Environment variable usage
- `.gitignore` for sensitive data
- Local storage only
- No external data sharing

---

**Last Updated**: December 2025  
**Version**: 1.0  
**Project**: Kaggle Agents Intensive Capstone
