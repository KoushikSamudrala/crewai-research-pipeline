from typing import List
from crewai import Agent, Crew, Process, Task, LLM
from crewai_tools import TavilySearchTool
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource

from src.services.rag import copy_pdfs_to_knowledge
from src.utils.config import settings
from src.utils.langsmith import configure_langsmith

configure_langsmith()

llm = LLM(
    model="gemini/gemini-1.5-pro",
    api_key=settings.GOOGLE_API_KEY,
    temperature=0.2,
)

embedder = {
    "provider": "google",
    "config": {
        "model": "models/text-embedding-004",
        "api_key": settings.GOOGLE_API_KEY,
    },
}


class ResearchCrew:
    def __init__(
        self,
        topic: str,
        use_web_search: bool = True,
        pdf_paths: List[str] | None = None,
    ):
        self.topic = topic
        self.use_web_search = use_web_search
        self.pdf_paths = pdf_paths or []

    def build(self):
        tools = []
        if self.use_web_search:
            tools.append(TavilySearchTool(api_key=settings.TAVILY_API_KEY))

        knowledge_sources = []
        copied = copy_pdfs_to_knowledge(self.pdf_paths)
        if copied:
            knowledge_sources.append(PDFKnowledgeSource(file_paths=copied))

        # ---------- Agents ----------
        researcher = Agent(
            role="Researcher",
            goal=(
                f"Gather authoritative, source-backed facts and recent developments "
                f"about: {self.topic}"
            ),
            backstory=(
                "You are a senior research specialist who mines the web and documents "
                "to surface high-signal, credible information."
            ),
            tools=tools,
            llm=llm,
            verbose=True,
        )

        analyst = Agent(
            role="Analyst",
            goal=(
                f"Synthesize research findings about '{self.topic}' into structured "
                "themes, tradeoffs, and actionable insights using step-by-step reasoning."
            ),
            backstory=(
                "You are a strategic analyst who applies chain-of-thought reasoning "
                "to uncover patterns and implications from complex information."
            ),
            llm=llm,
            verbose=True,
        )

        writer = Agent(
            role="Writer",
            goal=(
                f"Produce a professional, well-structured markdown research report "
                f"on '{self.topic}' based on the analyst's synthesis."
            ),
            backstory=(
                "You are a technical content writer who transforms analytical briefs "
                "into clear, polished reports for professional audiences."
            ),
            llm=llm,
            verbose=True,
        )

        # ---------- Tasks ----------
        research_task = Task(
            description=(
                f"Research the topic: '{self.topic}'.\n"
                "- Use Tavily web search to retrieve the latest news, papers, and "
                "expert commentary (if enabled).\n"
                "- If PDF documents are loaded, retrieve relevant context from them.\n"
                "- Collect at least 6 concrete facts, data points, or case studies "
                "with their sources."
            ),
            expected_output=(
                "Bullet-point research notes with cited sources, key quotes, "
                "statistics, and URLs where applicable."
            ),
            agent=researcher,
        )

        analysis_task = Task(
            description=(
                f"Analyze all research gathered on '{self.topic}'.\n"
                "Step 1 — Identify 4-5 dominant themes.\n"
                "Step 2 — For each theme, explain WHY it matters and WHAT its "
                "implications are (chain-of-thought).\n"
                "Step 3 — Note any contradictions, knowledge gaps, or risks.\n"
                "Step 4 — Rank themes by strategic importance."
            ),
            expected_output=(
                "A structured analytical brief with: thematic breakdown, "
                "reasoning chains, gap analysis, and ranked insights."
            ),
            agent=analyst,
            context=[research_task],
        )

        writing_task = Task(
            description=(
                f"Write a final research report on '{self.topic}' in markdown.\n\n"
                "Required sections:\n"
                "# {topic} — Research Report\n"
                "## Executive Summary\n"
                "## Key Findings\n"
                "## Trend & Theme Analysis\n"
                "## Actionable Recommendations\n"
                "## References\n\n"
                "Keep language concise and professional. Cite sources inline."
            ),
            expected_output=(
                "A complete markdown report (700-1500 words) with all sections "
                "populated, suitable for download and sharing."
            ),
            agent=writer,
            context=[research_task, analysis_task],
        )

        # ---------- Crew ----------
        return Crew(
            agents=[researcher, analyst, writer],
            tasks=[research_task, analysis_task, writing_task],
            process=Process.sequential,
            verbose=True,
            knowledge_sources=knowledge_sources,
            embedder=embedder,
        )

    def run(self) -> str:
        result = self.build().kickoff(inputs={"topic": self.topic})
        return getattr(result, "raw", str(result))
