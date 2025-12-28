from research_agent import search_arxiv_papers

papers = search_arxiv_papers("large language models")
for i,paper in enumerate(papers):
    print(f"\n--- Paper {i + 1} ---")
    print("Title:", paper["title"])
    print("Published:", paper["published"])
    print("Authors:", ", ".join(paper["authors"]))
    print("PDF URL:", paper["pdf_url"])
    print("Summary:", paper["summary"][:500], "...")