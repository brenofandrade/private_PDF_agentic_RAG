# Private PDF Agentic RAG

This project demonstrates an agent-powered retrieval augmented generation (RAG) pipeline for PDF files. The system uses [LangChain](https://github.com/langchain-ai/langchain) together with [Ollama](https://github.com/ollama/ollama) for local language models and [ChromaDB](https://github.com/chroma-core/chroma) as the vector store. A simple UI is provided using Streamlit.

## Features

- Upload PDF documents and split them into chunks.
- Store and persist document embeddings using ChromaDB.
- Query the documents through a LangChain agent that decides when to search the knowledge base.
- Interactive web interface built with Streamlit.

## Setup

1. Install dependencies (requires Python 3.10+):
   ```bash
   pip install -r requirements.txt
   ```
2. Make sure you have an Ollama model available (for example `llama2`). You can pull a model with:
   ```bash
   ollama pull llama2
   ```
3. Run the application:
   ```bash
   streamlit run app.py
   ```

Upload one or more PDF files, process them, and start asking questions.
