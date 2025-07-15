## 🧠 Multi-Tool Research Agent (PDF)

### 📥 Input

The user uploads a research paper in PDF format.

### 🔁 Workflow

1. **Text Extraction**
   The agent reads and extracts the full text content from the uploaded PDF.

2. **Domain Identification**
   It determines the research domain (e.g., Natural Language Processing, Biology, Computer Vision) based on the content.

3. **Tool Selection & Execution**

   * Uses a Large Language Model (LLM) to generate a concise summary of the paper.
   * Searches for cited or related papers using external search APIs.
   * Suggests **3 original follow-up research ideas or improvements** based on the content.

4. **Output Compilation**
   The agent compiles:

   * A domain classification
   * A research summary
   * Related works
   * Suggested research directions

   into a structured **Knowledge Digest** for the user.

