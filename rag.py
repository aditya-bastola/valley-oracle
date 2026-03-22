from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from utils.db import get_supabase_client

load_dotenv()

def retrieve_context(query: str) -> str:
    """Embed the query and return the top 5 matching chunks as a single string."""
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    query_vector = embeddings.embed_query(query)
    client = get_supabase_client()
    result = client.rpc("match_documents", {
        "query_embedding": query_vector,
        "match_count": 5,
    }).execute()
    return "\n\n".join([doc["content"] for doc in result.data])

SYSTEM_PROMPT = """
You are a ruthless, highly-experienced Silicon Valley veteran with decades
of experience building, funding, and shutting down startups. You speak with
brutal honesty and zero corporate politeness.

Answer the user's question strictly based on the context provided below.
If the answer is not present in the context, say so directly — do not
speculate, hallucinate, or draw on outside knowledge. Cite the ideas from
the context but do not quote it word for word.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "Context:\n{context}\n\nQuestion: {question}"),
])


llm = ChatOpenAI(model="gpt-4o-mini", streaming=True)


chain = (
    {"context": RunnableLambda(retrieve_context), "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

if __name__ == "__main__":
    question = "How do I come up with a good startup idea?"
    print(f"Question: {question}\n")
    for token in chain.stream(question):
        print(token, end="", flush=True)
    print()