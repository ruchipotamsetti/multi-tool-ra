import streamlit as st
from utils.text_tools import (
    extract_text_from_pdf,
    generate_related_paper_links,
    get_domain,
    summarize_text,
    generate_followups,
    extract_references,
    search_cited_papers,
    extract_keywords,
    extract_entities
)

st.set_page_config(page_title="Multi-Tool Research Assistant", layout="wide")
st.title("🧠 Multi-Tool Research Assistant")

uploaded_file = st.file_uploader("📄 Upload a Research PDF", type=["pdf"])

if uploaded_file:
    with st.expander("🧭 **View Processing Pipeline**", expanded=False):
        st.graphviz_chart("""
            digraph {
                "Upload PDF" -> "Extract Raw Text"
                "Extract Raw Text" -> "Summarize Text"
                "Summarize Text" -> "Detect Domain"
                "Summarize Text" -> "Extract Keywords"
                "Summarize Text" -> "Generate Follow-up Questions"
                "Summarize Text" -> "Extract Entities"
                "Extract Raw Text" -> "Extract Citations"
                "Extract Citations" -> "Search Cited Papers"
                "Detect Domain" -> "Generate Related Paper Links"
                "Extract Keywords" -> "Generate Related Paper Links"
            }
        """)

    with st.spinner("⚙️ Processing..."):
        raw_text = extract_text_from_pdf(uploaded_file)
        summary = summarize_text(raw_text)
        domain = get_domain(summary)
        keywords = extract_keywords(summary)
        related_url = generate_related_paper_links(domain, keywords)
        questions = generate_followups(summary)
        entities = extract_entities(summary)
        citations = extract_references(raw_text)
        cited_results = search_cited_papers(citations)

    st.markdown("## 📊 Processed Output")

    # 1. Summary + Domain + Follow-ups
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 🧾 Summary")
        st.write(summary)
        st.download_button("⬇️ Download Summary", summary, "summary.txt", mime="text/plain")

        st.markdown("### 🔑 Keywords")
        st.write(", ".join(keywords))
        st.download_button("⬇️ Download Keywords", "\n".join(keywords), "keywords.txt", mime="text/plain")

    with col2:
        st.markdown("### 🔍 Detected Domain")
        st.success(domain)

    st.divider()

    st.markdown("### 💡 Follow-up Research Questions")
    st.write(questions)
    st.download_button("⬇️ Download Questions", "\n".join(questions) if isinstance(questions, list) else str(questions),
                       "questions.txt", mime="text/plain")

    st.divider()

    st.markdown("### 📍 Named Entities (from Summary)")
    st.write(", ".join(entities))
    st.download_button("⬇️ Download Named Entities", "\n".join(entities), "entities.txt", mime="text/plain")

    st.divider()

    # st.markdown("### 🔗 Related Research Papers")
    # st.markdown(f"[🔍 Click here to search on Google Scholar]({related_url})")
    # st.download_button("⬇️ Download Search URL", related_url, "related_research_url.txt", mime="text/plain")

    # st.divider()

    st.markdown("### 🔎 Cited Papers")
    if cited_results==[]:
        st.write("No listed citations.")
    else:
        # for r in cited_results:
        #     st.markdown(f"- [{r['title']}]({r['link']})")
        citation_text = "\n".join([f"{r['title']} - {r['link']}" for r in cited_results])
        st.download_button("⬇️ Download Cited Papers", citation_text, "citations.txt", mime="text/plain")

    st.divider()

    with st.expander("📄 View Raw Extracted Text"):
        st.write(raw_text[:3000] + "..." if len(raw_text) > 3000 else raw_text)
