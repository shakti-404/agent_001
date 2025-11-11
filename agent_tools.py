# agent_tools.py
from typing import Dict, List
from ddgs import DDGS
import arxiv


class AgentTools:
    """Collection of tools for the agent."""

    def __init__(self):
        """Initialize the AgentTools instance."""
        pass

    def web_search(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search the web using DuckDuckGo (DDGS)."""
        if not query or not query.strip():
            return [{"error": "Empty search query"}]

        try:
            with DDGS() as ddgs:
                results = []
                for r in ddgs.text(query, max_results=max_results):
                    results.append({
                        "title": r.get("title", ""),
                        "link": r.get("href", ""),
                        "snippet": r.get("body", "")
                    })
                return results
        except Exception as e:
            return [{"error": f"Web search failed: {str(e)}"}]

    def research_paper_search(self, query: str, max_results: int = 1) -> List[Dict]:
        """Search academic research papers on arXiv."""
        if not query or not query.strip():
            return [{"error": "Empty research query"}]

        try:
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )

            results = []
            for paper in search.results():
                summary = paper.summary
                if len(summary) > 300:
                    summary = summary[:300] + "..."
                results.append({
                    "title": paper.title,
                    "authors": [author.name for author in paper.authors],
                    "summary": summary,
                    "published": paper.published.strftime("%Y-%m-%d"),
                    "link": paper.entry_id,
                    "pdf_url": paper.pdf_url
                })
            return results
        except Exception as e:
            return [{"error": f"Research paper search failed: {str(e)}"}]
