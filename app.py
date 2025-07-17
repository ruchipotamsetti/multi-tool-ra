import streamlit as st
from utils.text_tools import (
    extract_text_from_pdf,
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
    with st.spinner("Extracting text..."):
        raw_text = extract_text_from_pdf(uploaded_file)

    with st.expander("📄 Raw Extracted Text"):
        st.write(raw_text[:2000] + "...")  # show first part

    # Create two columns
    col1, col2 = st.columns(2)

    # LEFT COLUMN — core research tools
    with col1:
        if st.button("🔍 Detect Domain"):
            with st.spinner("Thinking..."):
                domain = get_domain(raw_text)
                st.success(f"Detected Domain: {domain}")

        if st.button("🧾 Summarize Paper"):
            with st.spinner("Summarizing..."):
                summary = summarize_text(raw_text)
                st.info(summary)
                st.download_button(
                    label="⬇️ Download Summary",
                    data=summary,
                    file_name="summary.txt",
                    mime="text/plain"
        )


        

        if st.button("💡 Suggest Research Questions"):
            with st.spinner("Generating ideas..."):
                questions = generate_followups(raw_text)
                st.write(questions)
                questions_text = "\n".join(questions) if isinstance(questions, list) else str(questions)
                st.download_button(
                    label="⬇️ Download Research Questions",
                    data=questions_text,
                    file_name="research_questions.txt",
                    mime="text/plain"
                )


        

    # RIGHT COLUMN — text analysis tools
    with col2:
        if st.button("🔎 Find Cited Papers"):
            with st.spinner("Extracting citations..."):
                citations = extract_references(raw_text)
                if not citations:
                    st.warning("No citations found.")
                else:
                    results = search_cited_papers(citations)
                    st.subheader("Top Cited Papers:")
                    for idx, r in enumerate(results):
                        st.markdown(f"- [{r['title']}]({r['link']})")

                    citation_text = "\n".join([f"{r['title']} - {r['link']}" for r in results])
                    st.download_button(
                        label="⬇️ Download Cited Papers",
                        data=citation_text,
                        file_name="cited_papers.txt",
                        mime="text/plain",
                        key="download_cited_papers"
                    )



        if st.button("🔑 Extract Keywords"):
            with st.spinner("Extracting..."):
                keywords = extract_keywords(raw_text)
                st.subheader("Top Keywords:")
                st.write(", ".join(keywords))

        if st.button("📍 Named Entities"):
            with st.spinner("Identifying entities..."):
                entities = extract_entities(raw_text)
                st.subheader("Named Entities (e.g., people, organizations, locations):")
                st.write(", ".join(entities))
