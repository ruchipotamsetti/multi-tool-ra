import fitz  # PyMuPDF
from groq import Groq
import os
from dotenv import load_dotenv

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
            "content": "You are a pirate.",
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
