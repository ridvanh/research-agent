from research_agent import search_arxiv_papers, summarize_paper
from slide_generator import generate_slide_deck

query = "graph neural networks"
papers = search_arxiv_papers(query)

for paper in papers:
    paper["summary"] = summarize_paper(paper)

generate_slide_deck(query, papers)
print("Slides generated: resarch_slides.pptx")