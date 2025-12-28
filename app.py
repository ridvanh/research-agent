import streamlit as st
from research_agent import search_arxiv_papers, summarize_paper
from slide_generator import generate_slide_deck
import os

st.set_page_config(page_title="Auto-Research Agent", layout="centered")

st.title("Auto-Research Agent")
st.write("Enter a research topic, and I'll fetch recent papers, summarize them, and generate a slide deck")

topic = st.text_input("Research Topic", value="transformer architecture")
generate_btn = st.button("Generate Slide Deck")

if generate_btn and topic:
    with st.spinner("Searching and summarizing papers..."):
        papers = search_arxiv_papers(topic)

        for paper in papers:
            paper["summary"] = summarize_paper(paper)

        file_path = generate_slide_deck(topic, papers)

    st.success("Slide deck generated!")

    with st.expander("View Paper Summaries"):
        for i, paper in enumerate(papers, start=1):
            st.subheader(f"Paper {i}: {paper['title']}")
            st.markdown(f"**Authors:** {', '.join(paper['authors'])}")
            st.markdown(f"**Published:** {paper['published']}")
            st.markdown(f"[PDF Link]({paper['pdf_url']})")
            st.text_area("Summary", paper['summary'], height=200)

    with open(file_path, "rb") as f:
        st.download_button(
            label="Download Slides",
            data=f,
            file_name="research_slides.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
