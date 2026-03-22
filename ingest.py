from langchain_openai import OpenAIEmbeddings
from utils.db import upsert_chunks
import time
import requests 
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

ESSAY_URLS = [
    ("http://www.paulgraham.com/startupideas.html",  "How to Get Startup Ideas"),
    ("http://www.paulgraham.com/growth.html",         "Startup = Growth"),
    ("http://www.paulgraham.com/ds.html",             "Do Things that Don't Scale"),
    ("http://www.paulgraham.com/ramenprofitable.html",          "Ramen Profitable"),
    ("http://www.paulgraham.com/before.html",         "Before the Startup"),
    ("http://www.paulgraham.com/good.html",           "Be Good"),
    ("http://www.paulgraham.com/hiring.html",         "Hiring is Obsolete"),
    ("http://www.paulgraham.com/avg.html",            "Beating the Averages"),
]

def scrape_essay(url: str, title: str) -> Document:
    """Fetch a Paul Graham essay and return a LangChain Document with metadata."""
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    font_tags = soup.find_all("font")
    text = max(font_tags, key=lambda tag: len(tag.get_text())).get_text(separator="\n", strip=True)
    return Document(page_content=text, metadata={"source": url, "title": title})

def chunk_documents(documents: list[Document]) -> list[Document]:
    """Chunk the documents into smaller chunks."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_documents(documents)

def embed_and_upsert(chunks: list[Document], batch_size: int = 50) -> None:
    """Embed chunks in batches and upsert them into Supabase."""
    model = OpenAIEmbeddings(model="text-embedding-3-small")
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        vectors = model.embed_documents([c.page_content for c in batch])
        upsert_chunks(batch, vectors)
        print(f"Upserted batch {i // batch_size + 1} ({len(batch)} chunks)")
        time.sleep(1)    

if __name__ == "__main__":
    docs = [scrape_essay(url, title) for url, title in ESSAY_URLS]
    chunks = chunk_documents(docs)
    print(f"Essays scraped: {len(docs)}")
    print(f"Total chunks:   {len(chunks)}")
    embed_and_upsert(chunks)
    print("Done.")