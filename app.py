import os
import streamlit as st
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.llms import Ollama

# Path where chroma will store the vectors
PERSIST_DIR = "db"
st.set_page_config(page_title="chatPDF", page_icon="🩺", layout="wide")
st.title("Assistente de documentos - Unimed Blumenau")

# Session state for the agent
if "agent" not in st.session_state:
    st.session_state.agent = None


uploaded_files = st.sidebar.file_uploader("Envie seus PDFs", accept_multiple_files=True, type=['pdf'])

if uploaded_files and st.button("Process Documents"):
    docs = []
    for uploaded_file in uploaded_files:
        loader = PyPDFLoader(uploaded_file)
        docs.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = text_splitter.split_documents(docs)

    embeddings = OllamaEmbeddings()

    if os.path.exists(PERSIST_DIR):
        db = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
    else:
        db = Chroma.from_documents(documents, embeddings, persist_directory=PERSIST_DIR)
    db.persist()

    retriever = db.as_retriever()
    llm = Ollama()
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    tools = [Tool(name="Document Search", func=qa_chain.run, description="Search through uploaded PDFs")]

    st.session_state.agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    st.success("Agent initialized!")

query = st.text_input("Ask a question about your documents")

if st.button("Submit Query") and query:
    if st.session_state.agent is None:
        st.warning("Please upload and process documents first.")
    else:
        answer = st.session_state.agent.run(query)
        st.write(answer)
