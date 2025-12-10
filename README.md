# AI Research Collaborator

**Multi-Agent Research Assistant for Education**

> A sophisticated AI-powered research system that automates academic research workflows using specialized agents to search, analyze, fact-check, and write research reports.

![Python](https://img.shields.io/badge/Python-3.9+-blue) ![License](https://img.shields.io/badge/License-MIT-green) ![Status](https://img.shields.io/badge/Status-Active-brightgreen)

---

## Table of Contents

- [Problem Statement](#problem-statement) - Challenges in academic research
- [Solution](#solution) - How AI Research Collaborator helps
- [Why Agents?](#why-agents) - Multi-agent architecture advantages
- [Architecture](#architecture) - System design and agent details
- [Features](#features) - Core capabilities and requirements
- [Installation](#installation) - Setup and configuration
- [Quick Start](#quick-start) - Get started in minutes
- [Usage Examples](#usage-examples) - Real-world use cases
- [Project Structure](#project-structure) - File organization
- [Kaggle Capstone](#kaggle-capstone-requirements) - Capstone requirements
- [Technical Details](#technical-details) - Technologies and patterns
- [Testing](#testing) - Running tests
- [Future Enhancements](#future-enhancements) - Roadmap
- [Contributing](#contributing) - How to contribute
- [License](#license) - MIT License
---

## Problem Statement

Academic research is a time-intensive and complex process that involves:

| Challenge | Description |
|-----------|-------------|
| **Information Overload** | Researchers sift through thousands of papers and articles |
| **Verification Challenges** | Ensuring accuracy and credibility of sources is difficult |
| **Time Constraints** | Students and educators have limited time for thorough research |
| **Synthesis Difficulty** | Combining information from multiple sources requires expertise |
| **Documentation Overhead** | Writing comprehensive reports takes significant effort |

### Current Impact

- **Time Investment**: 15-20 hours for comprehensive research
- **Scope Limitation**: Only 5-10 sources manually reviewed
- **Quality Variance**: Inconsistent fact-checking and verification
- **Resource Constraint**: Particularly challenging for under-resourced institutions

---

## Solution

The **AI Research Collaborator** is a multi-agent system that automates and accelerates the research workflow by combining specialized AI agents into a unified research pipeline.

### What It Does

| Feature | Description |
|---------|-------------|
| Automated Literature Search | Finds relevant academic papers and credible sources via Google Search |
| Intelligent Summarization | Analyzes and synthesizes findings from multiple sources |
| Fact-Checking | Validates claims and identifies contradictions with confidence ratings |
| Report Generation | Creates comprehensive, well-cited research reports |
| Memory Management | Remembers past research to provide context and improve future searches |

### Value Proposition

| Metric | Improvement |
|--------|-------------|
| Time Savings | 85% reduction - from 15-20 hours to 2-3 hours |
| Quality | Automated fact-checking improves overall accuracy |
| Coverage | Analyzes 10+ sources vs. 5-10 manual sources |
| Learning | Teaches research methodology through automated workflows |
| Reusability | Memory bank enables building on previous research |
| Cost | Reduces researcher/educator labor costs significantly |

---

## Why Agents?

### The Agent Advantage

This problem is uniquely suited for a multi-agent architecture:

| Advantage | Benefit |
|-----------|---------|
| Specialization | Each agent excels at a specific task (search, analyze, verify, write) |
| Parallel Processing | Multiple agents work on different aspects with coordinated workflow |
| Quality Control | Specialized agents provide checks and balances at each step |
| Scalability | Easy to add new agents for additional capabilities |
| Flexibility | Different workflows for different research needs and depths |

### Why Not a Single AI?

A single LLM struggles with:

- Diverse Skills: Research requires multiple distinct competencies
- Optimization: Sequential workflow benefits from specialized tuning per step
- Validation: Verification needs different approaches than content generation
- State Management: Complex memory and context handling across workflow

### Agent-Based Advantages

- Better Accuracy - Each agent optimized for its specific task
- More Comprehensive - Multiple perspectives and verification steps
- Clear Orchestration - Easy to understand and modify workflow
- Better Error Handling - Issues caught by verification agents

---

## Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR AGENT                       │
│                  (Workflow Coordinator)                     │
└────────────┬────────────────────────────────┬───────────────┘
                         │                                │
        ┌────────▼────────┐              ┌───────▼────────┐
        │  SEARCH AGENT   │              │ MEMORY MANAGER │
        │  Google Search  │              │ Session + Bank │
        └────────┬────────┘              └────────────────┘
                         │
        ┌────────▼────────┐
        │ SUMMARIZATION   │
        │     AGENT       │
        └────────┬────────┘
                         │
        ┌────────▼────────┐
        │  FACT-CHECKER   │
        │     AGENT       │
        └────────┬────────┘
                         │
        ┌────────▼────────┐
        │  WRITER AGENT   │
        │  Report Gen     │
        └─────────────────┘
```

### Agent Details

#### 1. Orchestrator Agent
- Role: Coordinates the entire research workflow
- Functions:
    - Plans research strategy
    - Delegates tasks to specialized agents
    - Manages data flow between agents
    - Synthesizes final results
- Type: Sequential agent with state management

#### 2. Literature Search Agent
- Role: Finds relevant research papers and articles
- Tools: Google Search (built-in tool)
- Functions:
    - Searches for academic papers
    - Identifies credible sources
    - Extracts metadata (title, authors, dates)
    - Prioritizes peer-reviewed content

#### 3. Summarization Agent
- Role: Analyzes and synthesizes research content
- Functions:
    - Summarizes individual papers
    - Identifies key findings
    - Synthesizes multiple sources
    - Highlights consensus and debates

#### 4. Fact-Checker Agent
- Role: Validates claims and ensures accuracy
- Tools: Google Search (for verification)
- Functions:
    - Verifies factual claims
    - Cross-references information
    - Identifies contradictions
    - Provides confidence ratings

#### 5. Writer Agent
- Role: Generates comprehensive research reports
- Functions:
    - Writes structured reports
    - Formats citations properly
    - Creates executive summaries
    - Maintains academic tone

### Memory System

#### Memory Bank (Long-term)
- Stores research history across sessions
- Enables retrieval of previous research
- Tracks research statistics
- Persistent JSON storage

#### Session Service (Short-term)
- Manages current research session
- Maintains workflow state
- Tracks session history
- Enables pause/resume functionality

---

## System Architecture

This section describes the system architecture, component responsibilities, and data flow for the AI Research Collaborator. A compact Mermaid diagram is provided for quick visual reference, followed by an ASCII overview and short deployment notes.

```mermaid
flowchart LR
    User[User / CLI / API] -->|requests| Orchestrator[Orchestrator Agent]
    Orchestrator -->|search tasks| Search[Search Agent]
    Orchestrator -->|summarize tasks| Summarizer[Summarization Agent]
    Orchestrator -->|verify tasks| FactChecker[Fact-Checker Agent]
    Orchestrator -->|compose report| Writer[Writer Agent]
    Search -->|store/retrieve| Memory[Memory Manager]
    Summarizer -->|store/retrieve| Memory
    FactChecker -->|store/retrieve| Memory
    Memory -->|context| Orchestrator
    Orchestrator -->|output files| Outputs[Outputs (reports / JSON)]
    Outputs -->|persist| Storage[Disk: outputs/ & memory_bank.json]
```

Simple ASCII overview:

```
User --> Orchestrator
Orchestrator -> Search -> Memory
Orchestrator -> Summarizer -> Memory
Orchestrator -> FactChecker -> Memory
Orchestrator -> Writer -> Outputs -> Storage
```

Key points:
- Orchestrator Agent: Central coordinator that accepts user requests (CLI/API), plans workflows, and dispatches tasks to specialized agents.
- Search Agent: Performs live web searches (Google Search API), extracts metadata and raw content.
- Summarization Agent: Condenses and synthesizes retrieved documents into structured summaries.
- Fact-Checker Agent: Validates claims by cross-referencing sources and assigns confidence scores.
- Writer Agent: Assembles final reports and formatted outputs (plain text, JSON); writes to `outputs/` and updates `memory_bank.json`.
- Memory Manager: Long-term JSON-backed memory and short-term session storage used for context, reuse, and audit trails.

Data flow and interactions:
- Requests enter via CLI or an API wrapper and are routed to the Orchestrator.
- The Orchestrator composes a workflow (search -> summarize -> verify -> write) and streams tasks to agents.
- Agents read/write structured artifacts to the Memory Manager to enable resumability and context-aware operations.
- Final outputs are persisted to the `outputs/` folder and the `memory_bank.json` for long-term retrieval.

Deployment & scaling notes:
- This project runs locally by default and requires an internet connection for search APIs.
- For higher throughput, containerize services (one container per major component) and run behind a lightweight task queue (Redis + RQ/Celery) with autoscaling.
- Use managed secrets or environment variables for API keys; do not commit secrets to the repo.

Security & observability:
- Store API keys in environment variables or `.env` (gitignored).
- Add structured logging for each agent and centralize logs with a log-collector (e.g., Filebeat -> Elasticsearch) for audit and debugging.
- Implement basic rate-limiting and retries for external API calls to handle transient failures gracefully.

---

## Features

### Core Capabilities

- Multi-Agent System - 5 specialized agents working in coordination
- Sequential Workflow - Orchestration and state management across agents
- Memory Persistence - Long-term research history with JSON storage
- Session Management - Short-term session state and pause/resume capability
- Flexible Depth - Quick (3 sources), Medium (5 sources), Deep (10 sources) research modes
- Fact-Checking - Automatic validation of claims with confidence ratings
- Report Generation - Academic-style reports with proper citations
- Memory Bank - Cross-session retrieval of previous research

---

## Installation

### Prerequisites

- Python 3.9 or higher
- Google API Key for Gemini (get it at [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey))
- Internet connection

### Setup Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/vengeanceprashlesh/AI-Researcher.git
   cd AI-Researcher
   ```

2. Set your Google API Key:
   ```bash
   # Option A: Set environment variable (Windows PowerShell)
   $env:GOOGLE_API_KEY="your-api-key-here"
   
   # Option B: Create .env file (recommended)
   cp .env.template .env
   # Edit .env and add your API key
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Quick Start

### Run Quick Demo
```bash
python demo.py
```

### Run Interactive Mode
```bash
python main.py
# Select option 6 for interactive mode
```

### Run Specific Example
```bash
python main.py
# Choose from:
# 1. Quick Research (3 sources, ~5 min)
# 2. Deep Research (10 sources, validation, report, ~20 min)
# 3. Comparative Research (compare 2+ topics)
# 4. Custom Workflow (build your own)
# 5. Memory Retrieval (view past research)
# 6. Interactive Mode (full conversation)
```

---

## Usage Examples

### In Python Code
```python
from agents import OrchestratorAgent
from memory_manager import ResearchMemoryManager

# Initialize
orchestrator = OrchestratorAgent()
memory = ResearchMemoryManager()

# Quick research
results = orchestrator.quick_research("Impact of AI on Education")
print(results)

# Deep research with all features
results = orchestrator.deep_research("Machine Learning in Healthcare")

# Save research
memory.start_research_session()
memory.save_research_to_session("My Topic", results)
memory.end_research_session()
```

### Web Interface (Optional)
```bash
python web_app.py
# Opens Gradio UI at http://localhost:7860
```

---

## Project Structure

```
kaggle-agent-project/
├── agents/                 # All agent implementations
│   ├── orchestrator_agent.py    # Main coordinator
│   ├── search_agent.py          # Literature search
│   ├── summarization_agent.py   # Content synthesis
│   ├── fact_checker_agent.py    # Verification
│   ├── writer_agent.py          # Report generation
│   └── __init__.py              # Module exports
├── config/
│   └── agent_config.py          # Configuration settings
├── main.py                 # Main application
├── demo.py                 # Quick demo
├── web_app.py              # Web UI (Gradio, optional)
├── memory_manager.py       # Memory system
├── requirements.txt        # Python dependencies
├── .env.template           # Environment variables template
├── README.md               # This file
├── ARCHITECTURE.md         # Detailed architecture docs
├── SETUP.md                # Setup guide
└── outputs/                # Generated reports (created at runtime)
```

---

## Kaggle Capstone Requirements

This project fulfills the Agents for Good (Education) capstone track requirements:

- Multi-Agent Architecture: 5 specialized agents coordinated by orchestrator
- Tool Use: Google Search API for literature search and fact verification
- Memory/Context: JSON-based memory bank and session service
- User Experience: CLI (main.py), Demo (demo.py), Web UI (web_app.py)
- Educational Value: Automates research workflow for students and educators
- Scalability: Designed for future cloud deployment and parallel processing

---

## Technical Details

### Technology Stack
- **Language**: Python 3.9+
- **LLM**: Google Gemini 2.0 Flash
- **API**: Google GenAI SDK
- **Storage**: JSON file-based
- **Web UI**: Gradio (optional)

### Design Patterns
- Multi-Agent Pattern: Specialized agents with clear responsibilities
- Orchestrator Pattern: Central coordinator managing workflow
- Repository Pattern: Memory Bank abstracts data persistence
- Chain-of-Responsibility: Sequential workflow between agents

### Temperatures Used
- Search Agent: 0.4 (balanced creativity and accuracy)
- Summarization Agent: 0.3 (factual, low variation)
- Fact-Checker Agent: 0.2 (highest precision)
- Writer Agent: 0.5 (creative but accurate)

---

## Testing

### Test Quick Research
```bash
python demo.py
```
Expected: Completes in ~2-5 minutes, shows summary

### Test Deep Research
```bash
python main.py
# Select option 2
```
Expected: Generates full report with validation

### Test Memory
```bash
python main.py
# Select option 5
```
Expected: Shows previous research sessions

### Test Interactive Mode
```bash
python main.py
# Select option 6
```
Expected: Interactive CLI prompt for research topics

---

## Future Enhancements

- **Parallel Agent Execution**: Run agents concurrently for faster research
- **Database Backend**: Replace JSON with PostgreSQL for scalability
- **Advanced Memory**: Semantic search and vector embeddings for memory retrieval
- **Multi-LLM Support**: Use different models for different agents
- **Export Formats**: PDF, Word, Markdown report generation
- **API Server**: REST API wrapper for web/mobile integration
- **Caching Layer**: Cache research results for identical topics
- **Authentication**: User accounts and private research histories
- **Rate Limiting**: Built-in throttling for API calls
- **Monitoring**: Dashboards for research metrics and agent performance

---

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## License

This project is licensed under the MIT License - see LICENSE file for details.

---

## Contact

For questions or feedback about this capstone project, please reach out through Kaggle.

---

**Made with care for Education**

*Empowering students and educators through AI-powered research automation*
