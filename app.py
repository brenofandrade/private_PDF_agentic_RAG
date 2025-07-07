import os
import tempfile

import streamlit as st
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.llms import Ollama

# Configurações
PERSIST_DIR = "db"
EMBEDDING_MODEL = "mxbai-embed-large"
CHAT_MODEL = "llama3.2:1b"

st.set_page_config(page_title="chatPDF", page_icon="🩺", layout="wide")
st.title("Assistente de documentos - Unimed Blumenau")

# Estados
if "agent" not in st.session_state:
    st.session_state.agent = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Upload e processamento dos PDFs
uploaded_files = st.sidebar.file_uploader(
    "📄 Envie seus PDFs", accept_multiple_files=True, type=['pdf']
)

if uploaded_files and st.sidebar.button("🔍 Processar Documentos"):
    docs = []
    for uploaded_file in uploaded_files:
        # Salva o arquivo em um temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name

        loader = PyPDFLoader(tmp_path)
        docs.extend(loader.load())
        os.unlink(tmp_path)  # remove temporário

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = text_splitter.split_documents(docs)

    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)

    if os.path.exists(PERSIST_DIR):
        db = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
    else:
        db = Chroma.from_documents(documents, embeddings, persist_directory=PERSIST_DIR)
    db.persist()

    retriever = db.as_retriever()
    llm = Ollama(model=CHAT_MODEL)
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    tools = [
        Tool(
            name="Document Search",
            func=qa_chain.run,
            description="Busca nos PDFs enviados"
        )
    ]

    st.session_state.agent = initialize_agent(
        tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
    )
    st.success("✅ Agente inicializado!")

# Caixa de chat
st.markdown("---")
st.subheader("💬 Pergunte sobre os documentos")

with st.container():
    for i, (user_msg, bot_msg) in enumerate(st.session_state.chat_history):
        st.markdown(f"**Você:** {user_msg}")
        st.markdown(f"**Assistente:** {bot_msg}")

    query = st.text_input("Digite sua pergunta e pressione Enter", key="chat_input")

    if query:
        if st.session_state.agent is None:
            st.warning("⚠️ Por favor, envie e processe documentos primeiro.")
        else:
            answer = st.session_state.agent.run(query)
            st.session_state.chat_history.append((query, answer))
            st.experimental_rerun()
