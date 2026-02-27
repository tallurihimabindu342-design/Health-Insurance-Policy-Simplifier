from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate


# -------- LOAD VECTORSTORE --------
def load_vectorstore():

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma(
        persist_directory="vectorstore",
        embedding_function=embeddings
    )

    return vectorstore


# -------- BUILD RAG --------
def build_rag_chain():

    vectorstore = load_vectorstore()

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 10}
    )

    prompt = PromptTemplate(
        input_variables=["context", "query"],
        template="""
You are a health insurance expert.

Use ONLY the provided policy context.

Rules:
- Start with YES or NO
- Explain simply
- Mention policy evidence
- If missing → say "Not found in document"

Context:
{context}

Question: {query}

Answer:
"""
    )

    llm = ChatOllama(
        model="gpt-oss:120b-cloud",
        temperature=0
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )

    return qa_chain


# -------- ASK FUNCTION --------
def ask_policy(question: str):

    chain = build_rag_chain()

    result = chain.invoke({"query": question})

    answer = result["result"]
    docs = result["source_documents"]

    citations = []
    for d in docs:
        citations.append({
            "page": d.metadata.get("page", "N/A"),
            "content": d.page_content[:300]
        })

    return answer, citations