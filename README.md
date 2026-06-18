# 🔬 CrewAI Multi-Agent Research & Content Pipeline

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![CrewAI](https://img.shields.io/badge/CrewAI-0.100+-orange)](https://crewai.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green)](https://fastapi.tiangolo.com)
[![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-yellow)](https://aws.amazon.com/lambda)
[![LangSmith](https://img.shields.io/badge/LangSmith-Monitoring-purple)](https://smith.langchain.com)

A production-grade multi-agent AI system where three specialized CrewAI agents — **Researcher**, **Analyst**, and **Writer** — autonomously collaborate to retrieve information, synthesize insights, and generate structured markdown reports on any custom topic.

---

## 🏗️ Architecture

```
Streamlit UI
│
▼
FastAPI Backend (Mangum → AWS Lambda)
│
▼
CrewAI Orchestration
├── Researcher ← Tavily Search + ChromaDB RAG
├── Analyst ← Chain-of-Thought synthesis
└── Writer ← Structured markdown report
│
▼
LangSmith (LLMOps Tracing)
```

---

## 📁 Project Structure

```
crewai-research-pipeline/
├── src/
│   ├── api/main.py           # FastAPI app + Mangum Lambda handler
│   ├── agents/crew.py        # CrewAI agents, tasks, pipeline
│   ├── services/rag.py       # PDF ingestion + directory management
│   └── utils/
│       ├── config.py         # Centralised settings from .env
│       └── langsmith.py      # LangSmith tracing setup
├── frontend/
│   ├── app.py                # Streamlit UI
│   └── .streamlit/config.toml
├── tests/test_api.py
├── scripts/
│   ├── run_local.sh          # One-command local dev launcher
│   └── deploy_lambda.sh      # AWS SAM deployment script
├── Dockerfile
├── template.yaml             # AWS SAM infrastructure
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## ⚙️ Prerequisites

- Python 3.11+
- Docker (for SAM builds)
- AWS CLI + SAM CLI (for Lambda deployment)
- API keys for:
  - [Google AI Studio](https://aistudio.google.com/) — Gemini
  - [Tavily](https://tavily.com/) — Web search
  - [LangSmith](https://smith.langchain.com/) — Tracing

---

## 🚀 Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/KoushikSamudrala/crewai-research-pipeline.git
cd crewai-research-pipeline
```

### 2. Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
```
Edit `.env` and fill in:
```env
GOOGLE_API_KEY=your_gemini_key
TAVILY_API_KEY=your_tavily_key
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_PROJECT=crewai-research-pipeline
```

**Get your Gemini key:** [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

**Get your Tavily key:** [app.tavily.com](https://app.tavily.com) → Dashboard → API Keys

**Get your LangSmith key:** [smith.langchain.com](https://smith.langchain.com) → Settings → API Keys

### 5. Run locally
```bash
chmod +x scripts/run_local.sh
./scripts/run_local.sh
```

| Service | URL |
|---------|-----|
| FastAPI backend | http://localhost:8000 |
| Swagger API docs | http://localhost:8000/docs |
| Streamlit frontend | http://localhost:8501 |

### 6. Test the API
```bash
# Health check
curl http://localhost:8000/health

# Text-only research
curl -X POST http://localhost:8000/research \
  -F "topic=Agentic AI trends in 2025" \
  -F "use_web_search=true"

# Research with PDF
curl -X POST http://localhost:8000/research/with-pdf \
  -F "topic=Key findings from this paper" \
  -F "use_web_search=true" \
  -F "files=@/path/to/paper.pdf"
```

### 7. Run tests
```bash
pytest tests/ -v
```

---

## ☁️ AWS Lambda Deployment

```bash
# Set credentials
export GOOGLE_API_KEY=...
export TAVILY_API_KEY=...
export LANGCHAIN_API_KEY=...

# Build and deploy
chmod +x scripts/deploy_lambda.sh
./scripts/deploy_lambda.sh
```

After deployment, copy the API Gateway URL from the SAM output and set it as `API_BASE_URL` in your Streamlit app or frontend `.env`.

---

## 📊 LangSmith Monitoring

1. Go to [smith.langchain.com](https://smith.langchain.com)
2. Open the `crewai-research-pipeline` project
3. View per-agent traces, token counts, latency, and LLM I/O for every run

---

## 🔧 Troubleshooting

| Issue | Fix |
|-------|-----|
| `GOOGLE_API_KEY not found` | Ensure `.env` is in project root |
| ChromaDB dimension mismatch | Delete `storage/` folder and restart |
| Lambda timeout | Increase `Timeout` in `template.yaml` (max 900s) |
| PDF not ingested | Ensure uploaded file ends with `.pdf` |
| LangSmith not tracing | Check `LANGCHAIN_TRACING_V2=true` in `.env` |

---

## 👤 Author

**Koushik Samudrala**  
M.Sc. Intelligent Systems · TU Kaiserslautern  
[GitHub](https://github.com/KoushikSamudrala)
