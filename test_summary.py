from research_agent import search_arxiv_papers, summarize_paper

papers = search_arxiv_papers("transformer architecture")

for paper in papers:
    print(f"\nTitle: {paper['title']}")
    print("Summary:\n")
    print(summarize_paper(paper))
    print("\n" + "-"*80 + "\n")