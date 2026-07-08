<div align="center">

# 🛠️ ResolveOps

**Multi-agent incident response automation powered by LangGraph**

_Classify → Investigate → Diagnose → Resolve → Notify — autonomously._

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Orchestration-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://github.com/langchain-ai/langgraph)
[![LangChain](https://img.shields.io/badge/LangChain-Framework-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://www.langchain.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

[![Gemini](https://img.shields.io/badge/Gemini-8E75B2?style=flat-square&logo=googlegemini&logoColor=white)](https://ai.google.dev/)
[![Groq](https://img.shields.io/badge/Groq-F55036?style=flat-square&logoColor=white)](https://groq.com/)
[![Mistral](https://img.shields.io/badge/Mistral-FA520F?style=flat-square&logo=mistralai&logoColor=white)](https://mistral.ai/)
[![DeepSeek](https://img.shields.io/badge/DeepSeek-536AF5?style=flat-square&logoColor=white)](https://huggingface.co/deepseek-ai)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Store-FF6F00?style=flat-square)](https://www.trychroma.com/)
[![LangSmith](https://img.shields.io/badge/LangSmith-Evaluation-1C3C3C?style=flat-square)](https://smith.langchain.com/)

[![Jira](https://img.shields.io/badge/Jira-0052CC?style=flat-square&logo=jira&logoColor=white)](https://www.atlassian.com/software/jira)
[![Confluence](https://img.shields.io/badge/Confluence-172B4D?style=flat-square&logo=confluence&logoColor=white)](https://www.atlassian.com/software/confluence)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/)
[![Slack](https://img.shields.io/badge/Slack-4A154B?style=flat-square&logo=slack&logoColor=white)](https://slack.com/)

</div>

---

## 📖 Overview

Modern incident response involves a lot of repetitive investigative work: reading the ticket, searching runbooks, checking recent deploys, correlating logs, and writing up a root cause before anyone can even start fixing the problem.

**ResolveOps automates that investigative loop** using a pipeline of specialized agents, each responsible for one step of the process, coordinated through a LangGraph state graph — from the first read of the ticket to the comment posted back on it.

---

## 🧭 Architecture

```
                              ┌────────────────┐
                              │      START      │
                              └────────┬────────┘
                                       ▼
                         ┌──────────────────────────┐
                         │    input_middleware       │──(blocked)──▶ END
                         │  PII redaction + guardrails│
                         └────────────┬─────────────┘
                                       ▼
                    ┌───────────────────────────────────┐
                    │           classifier               │  categorize type, severity,
                    └────────────────┬────────────────────┘  affected systems
                                       ▼
                    ┌───────────────────────────────────┐
                    │            retriever                │  RAG search over
                    └────────────────┬────────────────────┘  knowledge base
                                       ▼
                    ┌───────────────────────────────────┐
                    │          investigation              │  tool-calling agent:
                    │   (GitHub + Confluence tool calls)   │  commits, issues, PRs, docs
                    └────────────────┬────────────────────┘
                                       ▼
                    ┌───────────────────────────────────┐
                    │           root_cause                │  most likely root cause
                    └────────────────┬────────────────────┘
                                       ▼
                    ┌───────────────────────────────────┐
                    │            reflection                │  critiques the analysis
                    └────────────────┬────────────────────┘  for gaps & inconsistencies
                                       ▼
                    ┌───────────────────────────────────┐
                    │             solution                 │  schema-validated
                    └────────────────┬────────────────────┘  recommended fix
                                       ▼
                         ┌──────────────────────────┐
                         │    output_middleware       │──(blocked)──▶ END
                         │  schema validation + PII   │
                         └────────────┬─────────────┘
                                       ▼
                    ┌───────────────────────────────────┐
                    │           jira_update                │  posts resolution
                    └────────────────┬────────────────────┘  as a ticket comment
                                       ▼
                    ┌───────────────────────────────────┐
                    │       slack_notification              │  notifies the team
                    └────────────────┬────────────────────┘  channel
                                       ▼
                              ┌────────────────┐
                              │       END        │
                              └────────────────┘
```

Each node reads and writes to a shared `state` object that flows through the graph, so every downstream agent has full context from everything that came before it.

---

## ✨ Key Features

|                                         |                                                                                                                       |
| --------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| 🧩 **Multi-agent pipeline**             | Eight specialized agents, each with a single responsibility, orchestrated via LangGraph                               |
| 🔧 **Tool-calling investigation agent** | Dynamically queries GitHub (commits, PRs, issues, files) and Confluence rather than relying on static retrieval alone |
| 📚 **Retrieval-Augmented Generation**   | ChromaDB vector store with local HuggingFace embeddings over an ingested knowledge base                               |
| 🔀 **Multi-provider LLM routing**       | Tasks routed to different models by reasoning need, with automatic fallback if the primary fails                      |
| ✅ **Schema-validated outputs**         | Final solutions validated against a Pydantic schema before reaching Jira/Slack                                        |
| 🛡️ **Middleware layer**                 | PII redaction, prompt-injection guardrails, and output validation wrap the core pipeline                              |
| 📊 **Evaluation harness**               | LangSmith-backed dataset and evaluators for tracking pipeline quality over time                                       |
| 🩹 **Graceful degradation**             | External tool failures are caught and surfaced as structured errors, never crash the run                              |

---

## 🏗️ Tech Stack

| Layer             | Technology                                                    |
| ----------------- | ------------------------------------------------------------- |
| **Orchestration** | LangGraph, LangChain                                          |
| **LLMs**          | Gemini · Groq · Mistral · DeepSeek (via Hugging Face)         |
| **Vector store**  | ChromaDB                                                      |
| **Embeddings**    | `BAAI/bge-small-en-v1.5` (local, via `sentence-transformers`) |
| **Evaluation**    | LangSmith                                                     |
| **Integrations**  | Jira · Confluence · GitHub · Slack                            |
| **Validation**    | Pydantic                                                      |
| **Language**      | Python 3.11+                                                  |

---

## 📁 Project Structure

```
RESOLVEOPS/
├── agents/                   # One file per pipeline stage
│   ├── ticket_classifier_agent.py
│   ├── rag_retrieval_agent.py
│   ├── investigation_agent.py
│   ├── root_cause_agent.py
│   ├── reflection_agent.py
│   ├── solution_agent.py
│   ├── jira_update_agent.py
│   └── slack_notification_agent.py
├── graphs/                   # LangGraph wiring
│   ├── nodes.py
│   └── workflow.py
├── middleware/                # Pre/post-processing
│   ├── input_middleware.py
│   ├── output_middleware.py
│   ├── pii_middleware.py
│   └── guardrails.py
├── prompts/                   # System prompts per agent
├── rag/                       # Embeddings, vector store, ingestion, retrieval
│   ├── embeddings.py
│   ├── vectordb.py
│   ├── ingest.py
│   └── retriever.py
├── tools/                     # External integrations + LLM router
│   ├── jira_tool.py
│   ├── github_tool.py
│   ├── confluence_tool.py
│   ├── slack_tool.py
│   ├── investigation_tools.py
│   └── litellm_router.py
├── schemas/                   # Pydantic/typed state and data models
│   ├── ticket_schema.py
│   ├── solution_schema.py
│   └── state_schema.py
├── evaluation/                 # LangSmith dataset, evaluators, runner
│   ├── dataset.py
│   ├── evaluators.py
│   └── run_eval.py
├── tests/                     # Test suite
├── main.py                     # Entry point
└── .env                        # Environment configuration (not committed)
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- API keys for the services you want active: Google (Gemini), Groq, Mistral, Hugging Face, GitHub, Atlassian (Jira + Confluence), and Slack

### Installation

```bash
git clone https://github.com/your-username/resolveops.git
cd resolveops
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```dotenv
# ── LLM Providers ──────────────────────────
GOOGLE_API_KEY=
GROQ_API_KEY=
MISTRAL_API_KEY=
HUGGINGFACEHUB_API_TOKEN=

# ── GitHub ──────────────────────────────────
GITHUB_TOKEN=

# ── Jira ────────────────────────────────────
JIRA_SERVER=
JIRA_EMAIL=
JIRA_API_TOKEN=

# ── Confluence ──────────────────────────────
CONFLUENCE_URL=
CONFLUENCE_EMAIL=
CONFLUENCE_API_TOKEN=

# ── Slack ───────────────────────────────────
SLACK_BOT_TOKEN=
SLACK_CHANNEL_ID=

# ── LangSmith (evaluation) ──────────────────
LANGSMITH_API_KEY=
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=ResolveOps
```

> 💡 Any integration left blank degrades gracefully rather than crashing the pipeline — see [Middleware & Guardrails](#️-middleware--guardrails).

### Ingesting a Knowledge Base

Before running the pipeline, populate the vector store with runbooks or past incident docs:

```bash
python -c "from rag.ingest import DocumentIngestor; DocumentIngestor().ingest('path/to/your/document.md')"
```

### Running the Pipeline

```bash
python main.py
```

Runs a sample incident ticket through the full graph and prints the final state — classification, investigation, root cause, generated solution, and integration results.

---

## 📊 Running Evaluations

With LangSmith configured:

```bash
python -m evaluation.run_eval
```

Builds (or reuses) a benchmark dataset of sample tickets, runs the full graph against each one, and scores the results against a set of evaluators — schema validity, confidence thresholds, pipeline completion, and an LLM-as-judge check on root cause plausibility.

---

## 🛡️ Middleware & Guardrails

- **`input_middleware`** — redacts PII from the incoming ticket and runs prompt-injection/length guardrails before anything reaches an LLM
- **`output_middleware`** — validates the generated solution against the required schema and redacts PII before it's posted externally
- Both stages can short-circuit the graph (`blocked = True`), skipping straight to the end without ever calling Jira or Slack

---

## 🗺️ Roadmap

- [ ] Human-in-the-loop approval gate before Jira/Slack updates (`interrupt()`-based)
- [ ] Expanded test coverage
- [ ] Additional evaluators (Jira comment quality, timeline coherence)

---

## 📄 License

MIT — see [LICENSE](LICENSE) for details.

<div align="center">

_Built with LangGraph 🦜🔗_

</div>
