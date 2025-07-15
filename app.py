import streamlit as st
from utils.text_tools import extract_text_from_pdf, get_domain, summarize_text, generate_followups, extract_references, search_cited_papers

st.set_page_config(page_title="Multi-Tool Research Assistant", layout="wide")
st.title("🧠 Multi-Tool Research Assistant")

uploaded_file = st.file_uploader("Upload a Research PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting text..."):
        raw_text = extract_text_from_pdf(uploaded_file)

    with st.expander("📄 Raw Extracted Text"):
        st.write(raw_text[:2000] + "...")  # show first part

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔍 Detect Domain"):
            with st.spinner("Thinking..."):
                domain = get_domain(raw_text)
                st.success(f"Detected Domain: {domain}")

    with col2:
        if st.button("🧾 Summarize Paper"):
            with st.spinner("Summarizing..."):
                summary = summarize_text(raw_text)
                st.info(summary)

    if st.button("💡 Suggest Research Questions"):
        with st.spinner("Generating ideas..."):
            questions = generate_followups(raw_text)
            st.write(questions)

    if st.button("🔎 Find Cited Papers"):
        with st.spinner("Extracting citations..."):
            citations = extract_references(raw_text)
            if not citations:
                st.warning("No citations found.")
            else:
                results = search_cited_papers(citations)
                st.subheader("Top Cited Papers:")
                for r in results:
                    st.markdown(f"- [{r['title']}]({r['link']})")
