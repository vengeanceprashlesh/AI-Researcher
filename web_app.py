"""
Web Interface for AI Research Collaborator

Runs the multi-agent research assistant behind a simple web UI.

This file is optional for the Kaggle capstone (deployment bonus) but
provides a clean example of how to expose the agent via HTTP.

Usage (local):
    python web_app.py
Then open the URL that Gradio prints in your browser.
"""

import os
from typing import Tuple

import gradio as gr

from agents import OrchestratorAgent
from memory_manager import ResearchMemoryManager


# Global, long-lived instances so we can reuse memory across calls
memory_manager = ResearchMemoryManager()
# Orchestrator requires a valid GOOGLE_API_KEY, so we lazy-load it
# after verifying the key is present.
orchestrator = None


def _ensure_api_key() -> Tuple[bool, str]:
    """Check that GOOGLE_API_KEY is set, return (ok, message)."""
    if not os.getenv("GOOGLE_API_KEY"):
        # Do NOT print or log any key values, just a friendly error.
        msg = (
            "GOOGLE_API_KEY environment variable is not set.\n\n"
            "Set it before launching the app, for example:\n"
            "  Windows PowerShell:  $env:GOOGLE_API_KEY='your-key-here'\n"
            "  Linux/Mac:          export GOOGLE_API_KEY='your-key-here'"
        )
        return False, msg
    return True, "OK"


def get_orchestrator() -> OrchestratorAgent:
    """Get a global OrchestratorAgent instance, creating it on first use."""
    global orchestrator
    if orchestrator is None:
        orchestrator = OrchestratorAgent()
    return orchestrator


def run_research(topic: str, depth: str, validate: bool, generate_report: bool):
    """Gradio callback: run a research job and return outputs.

    Returns a tuple of (search_results, summary, validation_report, full_report, metadata_text).
    """
    ok, msg = _ensure_api_key()
    if not ok:
        return "", "", "", msg

    topic = topic.strip()
    if not topic:
        return "", "", "", "Please enter a research topic."

    # Start a named session for the web UI
    session_id = memory_manager.start_research_session("web_ui_session")

    try:
        orc = get_orchestrator()
        results = orc.conduct_research(
            topic=topic,
            depth=depth,
            validate=validate,
            generate_report=generate_report,
        )

        # Persist to memory bank
        memory_manager.save_research_to_session(topic, results)

        search_results = results.get("search_results", {}).get("search_results", "")
        summary = results.get("summary", {}).get("summary", "")
        validation_report = results.get("validation", {}).get("validation_report", "")
        full_report = results.get("report", {}).get("report", "")

        ctx = memory_manager.get_research_context()
        stats = ctx["statistics"]
        metadata = (
            f"Session: {session_id}\n"
            f"Total sessions in memory: {stats['total_research_sessions']}\n"
            f"Unique topics: {stats['unique_topics']}\n"
            f"Most researched topic: {stats['most_researched']}"
        )

        return search_results, summary, validation_report, full_report, metadata

    except Exception as e:  # Surface clean error to UI
        return "", "", "", "", f"Error while running research: {e}"

    finally:
        memory_manager.end_research_session()


def build_interface() -> gr.Blocks:
    """Create the Gradio UI layout."""

    theme = gr.themes.Soft(primary_hue="orange", neutral_hue="slate")

    with gr.Blocks(title="AI Research Collaborator", theme=theme) as demo:
        gr.Markdown(
            """# 🎓 AI Research Collaborator
Multi-agent research assistant for education.

**How to use it**
1. Enter your research topic on the left.
2. Choose research depth and whether to fact-check / write a full report.
3. Click **Run Research** to see results on the right.
"""
        )

        with gr.Row():
            # Left column: controls
            with gr.Column(scale=1, min_width=320):
                gr.Markdown("### 🔍 Research setup")
                topic = gr.Textbox(
                    label="Research topic",
                    placeholder="e.g., Impact of AI on personalized learning",
                    lines=2,
                )
                depth = gr.Radio(
                    ["quick", "medium", "deep"],
                    value="medium",
                    label="Research depth",
                    info="Quick = 3 sources, Medium = 5, Deep = 10 (with full report)",
                )
                validate = gr.Checkbox(value=True, label="Run fact-checking")
                generate_report = gr.Checkbox(
                    value=True,
                    label="Generate full report",
                    info="Turn off for faster, summary-only runs.",
                )
                run_button = gr.Button("🚀 Run Research", variant="primary")
                gr.Markdown(
                    "Tip: use **deep** for final results and **quick** while exploring topics."
                )

            # Right column: results
            with gr.Column(scale=2):
                gr.Markdown("### 📊 Results")
                with gr.Tab("Summary"):
                    summary_out = gr.Textbox(
                        label="High-level summary",
                        lines=16,
                        show_copy_button=True,
                    )
                with gr.Tab("Full Report"):
                    report_out = gr.Textbox(
                        label="Full report (ready to paste into a doc)",
                        lines=22,
                        show_copy_button=True,
                    )
                with gr.Tab("Validation"):
                    validation_out = gr.Textbox(
                        label="Fact-checking & validation report",
                        lines=16,
                        show_copy_button=True,
                    )
                with gr.Tab("Sources"):
                    sources_out = gr.Textbox(
                        label="Search results (raw, for citations / debugging)",
                        lines=16,
                        show_copy_button=True,
                    )
                with gr.Tab("Session & Memory"):
                    meta_out = gr.Textbox(
                        label="Session & memory info",
                        lines=8,
                        show_copy_button=True,
                    )

        run_button.click(
            fn=run_research,
            inputs=[topic, depth, validate, generate_report],
            outputs=[sources_out, summary_out, validation_out, report_out, meta_out],
        )

    return demo


if __name__ == "__main__":
    # For local runs only. On Kaggle/Cloud Run, call build_interface().launch()
    app = build_interface()
    app.launch()
