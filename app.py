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
    extract_entities,
)

st.set_page_config(page_title="Multi-Tool Research Assistant", layout="wide")
st.title("🧠 Multi-Tool Research Assistant")

uploaded_file = st.file_uploader("Upload a Research PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Processing..."):
        # Step 1: Extract raw text
        raw_text = extract_text_from_pdf(uploaded_file)

        # Step 2: Summarize raw text
        summary = summarize_text(raw_text)

        # Step 3: Detect domain from summary
        domain = get_domain(summary)

        # Step 4: Extract keywords from summary
        keywords = extract_keywords(summary)

        related_url = generate_related_paper_links(domain, keywords)

        # Step 5: Generate follow-up questions from summary
        questions = generate_followups(summary)

        # Step 6: Extract entities from summary
        entities = extract_entities(summary)

        # Step 7: Extract citations from raw text (more reliable than summary)
        citations = extract_references(raw_text)
        cited_results = search_cited_papers(citations)

    # === Display Results ===

    st.subheader("📄 Raw Extracted Text")
    st.write(raw_text[:2000] + "...")

    st.subheader("🧾 Summary")
    st.write(summary)
    st.download_button("⬇️ Download Summary", summary, "summary.txt", mime="text/plain", key="summary")

    st.subheader("🔍 Detected Domain")
    st.success(domain)

    st.subheader("💡 Follow-up Research Questions")
    st.write(questions)
    st.download_button("⬇️ Download Questions", "\n".join(questions) if isinstance(questions, list) else str(questions),
                       "questions.txt", mime="text/plain", key="questions")

    st.subheader("🔑 Extracted Keywords")
    st.write(", ".join(keywords))
    st.download_button("⬇️ Download Keywords", "\n".join(keywords), "keywords.txt", mime="text/plain", key="keywords")

    st.subheader("🔗 Related Research Papers")
    st.markdown(f"🔍 [Click here to search related papers on Google Scholar]({related_url})")

    st.download_button(
        label="⬇️ Download Related Search URL",
        data=related_url,
        file_name="related_research_url.txt",
        mime="text/plain",
        key="related_url"
    )

    st.subheader("📍 Named Entities (from summary)")
    st.write(", ".join(entities))
    st.download_button("⬇️ Download Named Entities", "\n".join(entities), "entities.txt", mime="text/plain", key="entities")

    st.subheader("🔎 Cited Papers")
    for r in cited_results:
        st.markdown(f"- [{r['title']}]({r['link']})")
    citation_text = "\n".join([f"{r['title']} - {r['link']}" for r in cited_results])
    st.download_button("⬇️ Download Cited Papers", citation_text, "citations.txt", mime="text/plain", key="citations")

    
