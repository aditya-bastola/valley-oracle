# 🏺 ValleyOracle

**The RAG-powered mentor that thinks like a Silicon Valley legend.**

ValleyOracle is a specialized AI advisor built to provide high-signal startup advice. Unlike generic LLMs, it is grounded strictly in the collective wisdom of elite founders—starting with the complete essays of **Paul Graham** 

---

## 🚀 The Tech Stack

* **Language:** Python 3.11+
* **Orchestration:** [LangChain](https://www.langchain.com/) (RAG Pipeline)
* **Vector Database:** [Supabase](https://supabase.com/) with `pgvector`
* **Embeddings:** OpenAI `text-embedding-3-small`
* **LLM:** OpenAI `gpt-4o-mini`
* **Frontend:** [Streamlit](https://streamlit.io/)

---

## 🛠️ How It Works

1.  **Ingestion:** A custom Python script scrapes and cleans source material (essays, transcripts). 
2.  **Chunking:** Documents are split using `RecursiveCharacterTextSplitter` to maintain semantic context.
3.  **Vectorization:** Text chunks are converted into 1536-dimensional vectors via OpenAI.
4.  **Storage:** Vectors and metadata are stored in Supabase using the `pgvector` extension.
5.  **Retrieval:** When a user asks a question, we perform a similarity search to find the most relevant advice.
6.  **Synthesis:** The LLM generates a response formatted in the "Founder Mode" tone, citing its sources.

---

## 🏃 Quick Start


```bash
1. Clone the repo
git clone [https://github.com/YOUR-USERNAME/valley-oracle.git](https://github.com/YOUR-USERNAME/valley-oracle.git)
cd valley-oracle

2. Install dependencies
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

3. Environment Setup
Create a .env file and add your credentials:
OPENAI_API_KEY=your_key_here
SUPABASE_URL=your_url_here
SUPABASE_SERVICE_KEY=your_key_here

4. Run the App
streamlit run app.py



