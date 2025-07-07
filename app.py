import streamlit as st
import time

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

    with st.spinner("Aguarde..."):
        time.sleep(5)




# Caixa de chat
st.markdown("---")
st.subheader("💬 Pergunte sobre os documentos")

with st.container():
    

    query = st.chat_input(placeholder="Qual é a sua pergunta?...", key="chat_input")

    