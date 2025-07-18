import fitz  # PyMuPDF
from groq import Groq
import os
import re
from dotenv import load_dotenv
import spacy

from sklearn.feature_extraction.text import TfidfVectorizer
import re

def extract_text_from_pdf(pdf_file):
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

load_dotenv()
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def ask_llm(prompt):
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        },
        {
            "role": "system",
            "content": "You are an assistant.",
        }
    ],
    model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content

def get_domain(text):
    prompt = f"Determine the research domain (e.g., NLP, CV, Bioinformatics, etc.) for the following abstract or intro:\n\n{text[:1000]}"
    return ask_llm(prompt)

def summarize_text(text):
    prompt = f"Summarize this research paper in a concise paragraph:\n\n{text[:2000]}"
    return ask_llm(prompt)

def generate_followups(text):
    prompt = f"Based on this research paper, suggest 3 original follow-up research questions:\n\n{text[:2000]}"
    return ask_llm(prompt)

def extract_references(text: str) -> list:
    # Locate the start of the references section
    refs_start = re.search(r'(References|Bibliography|REFERENCES)', text)
    if not refs_start:
        return []

    start = refs_start.start()
    references_text = text[start:]

    # Define common section headers that might follow References
    end_section_pattern = re.compile(
        r'\n\s*(Appendix|Acknowledgements?|Supplementary\s+Information|Funding|Author Contributions|Conflict of Interest|Footnotes|About the Authors)\s*\n',
        re.IGNORECASE
    )

    # Truncate the references section if any of those headers appear
    end_match = end_section_pattern.search(references_text)
    if end_match:
        references_text = references_text[:end_match.start()]

    # Pattern for numbered references: [1], [2], or 1. 2. etc.
    ref_pattern = re.compile(r'(?=\n?(?:\[\d+\]|\d{1,2}\.))', re.MULTILINE)

    # Split based on that pattern
    raw_refs = ref_pattern.split(references_text)

    # Clean and filter references
    clean_refs = []
    for ref in raw_refs:
        ref = ref.strip()
        if len(ref) > 50:
            # Remove leading [1], 1., 12., etc.
            cleaned = re.sub(r'^(\[\d+\]|\d{1,2}\.)\s*', '', ref)
            cleaned = cleaned.replace("&", "")
            clean_refs.append(cleaned)

    # for ref in clean_refs:
    #     print(ref)

    return clean_refs[:10]


def search_cited_papers(citations: list) -> list:
    # Fake search results — replace with actual API calls
    results = []
    for citation in citations:
        results.append({
            "title": citation[:80] + "...",
            "link": f"https://scholar.google.com/scholar?q={citation.replace(' ', '+')}"
        })
    return results


def extract_keywords(text, top_n=10):
    from collections import Counter

    # Basic tokenizer
    words = re.findall(r'\b\w+\b', text.lower())
    stopwords = set(TfidfVectorizer(stop_words='english').get_stop_words())

    filtered = [w for w in words if w not in stopwords and len(w) > 3]
    common = Counter(filtered).most_common(top_n)
    return [word for word, freq in common]



nlp = spacy.load("en_core_web_sm")

def extract_entities(text, entity_types=["PERSON", "ORG", "GPE", "DATE"]):
    doc = nlp(text)
    ents = [ent.text for ent in doc.ents if ent.label_ in entity_types]
    return list(set(ents))[:20]  # limit to unique top 20

