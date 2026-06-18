import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(
    page_title="CrewAI Research Pipeline",
    page_icon="🔬",
    layout="wide",
)

st.title("🔬 CrewAI Multi-Agent Research & Content Pipeline")
st.caption("Powered by Gemini 1.5 Pro · Tavily Search · ChromaDB · LangSmith")
st.divider()

# ---------- Sidebar ----------
with st.sidebar:
    st.header("⚙️ Options")
    use_web_search = st.toggle("Enable Tavily Web Search", value=True)
    st.markdown("---")
    st.markdown("**Upload PDFs (optional)**")
    uploaded_files = st.file_uploader(
        "Add knowledge documents",
        type=["pdf"],
        accept_multiple_files=True,
    )
    st.markdown("---")
    st.markdown(
        "**Pipeline:**\n"
        "1. 🔍 Researcher gathers data\n"
        "2. 🧠 Analyst synthesizes insights\n"
        "3. ✍️ Writer produces markdown report"
    )

# ---------- Main ----------
topic = st.text_area(
    "🎯 Enter your research topic",
    placeholder="e.g. Latest advances in multi-agent AI systems 2025",
    height=100,
)

run_btn = st.button("🚀 Generate Report", type="primary")

if run_btn:
    if not topic.strip():
        st.warning("Please enter a topic before running.")
        st.stop()

    with st.spinner("Agents are working… this may take 1–3 minutes."):
        try:
            data = {
                "topic": topic,
                "use_web_search": str(use_web_search).lower(),
            }

            if uploaded_files:
                files_payload = [
                    ("files", (f.name, f.getvalue(), "application/pdf"))
                    for f in uploaded_files
                ]
                resp = requests.post(
                    f"{API_BASE_URL}/research/with-pdf",
                    data=data,
                    files=files_payload,
                    timeout=300,
                )
            else:
                resp = requests.post(
                    f"{API_BASE_URL}/research",
                    data=data,
                    timeout=300,
                )

            resp.raise_for_status()
            payload = resp.json()

            st.success(
                f"✅ Report generated! "
                f"PDFs ingested: {payload.get('pdfs_ingested', 0)}"
            )
            st.divider()
            st.markdown("## 📄 Research Report")
            st.markdown(payload["report"])
            st.download_button(
                label="⬇️ Download as Markdown",
                data=payload["report"],
                file_name=f"report_{topic[:40].replace(' ', '_')}.md",
                mime="text/markdown",
            )

        except requests.exceptions.Timeout:
            st.error("Request timed out. The pipeline is still running — try again.")
        except Exception as exc:
            st.error(f"Error: {exc}")
