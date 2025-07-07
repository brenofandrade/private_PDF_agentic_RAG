import streamlit as st

st.set_page_config(page_title="Assistente de documentos - Unimed Blumenau", layout="wide")

st.title("Assistente de documentos - Unimed Blumenau")

st.sidebar.header("Upload de Documentos")
uploaded_files = st.sidebar.file_uploader("Envie seus PDFs", accept_multiple_files=True, type=['pdf'])


user_input = st.chat_input("Digite sua pergunta")
if user_input:
    # Aqui iria a lógica de consulta aos documentos e geração da resposta.
    st.write(f"Você perguntou: {user_input}")

