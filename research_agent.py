import arxiv
from langchain.chat_models import ChatOllama
from langchain.schema import HumanMessage

def search_arxiv_papers(topic: str, max_results: int = 5):
    search = arxiv.Search(
        query=f'ti:"{topic}" OR abs:"{topic}" OR cat:cs.LG OR cat:cs.AI',
        max_results=max_results,
        sort_order=arxiv.SortOrder.Descending
    )

    papers = []
    for result in search.results():
        if (topic.lower() in result.title.lower()) or ("survey" in result.title.lower() or "review" in result.title.lower()):
            papers.append({
                "title": result.title,
                "summary": result.summary,
                "authors": [author.name for author in result.authors],
                "pdf_url": result.pdf_url,
                "published": result.published.strftime("%Y-%m-%d")
            })

    return papers

llm = ChatOllama(model="mistral")

def summarize_paper(paper: dict) -> str:
    prompt = f"""
    Summarize this paper for a slide. Include:
     - What the paper is about
     - The problem it solves
     - Main method and results
    
    Title: {paper["title"]}
    
    Abstract:
    {paper["summary"]}
    """

    response = llm([HumanMessage(content=prompt)])
    return response.content