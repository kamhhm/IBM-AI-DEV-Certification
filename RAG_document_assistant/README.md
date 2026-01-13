# RAG Document Assistant

> Part of the [IBM AI Developer Professional Certificate](https://www.coursera.org/professional-certificates/applied-artifical-intelligence-ibm-watson-ai)

A tool to help developers learn technical documentation faster. Upload any PDF—API docs, SDK guides, or technical specs—and ask questions in plain English. The app uses Retrieval-Augmented Generation (RAG) to find relevant sections and generate accurate answers.

Built with Flask on the backend, using LangChain to orchestrate the RAG pipeline. Documents are embedded using HuggingFace's sentence-transformers and stored in ChromaDB for semantic search. The LLM (Falcon-7B via HuggingFace) generates answers based on retrieved context.

## Features

- Upload PDF documents
- Ask questions and get AI-generated answers
- Uses semantic search to find relevant content
- Maintains conversation history

## Project Structure

```
├── app/
│   ├── config.py          # Configuration
│   ├── main.py            # Flask routes
│   └── services/
│       ├── llm.py         # LLM setup
│       └── rag.py         # RAG pipeline
├── static/                # CSS, JS
├── templates/             # HTML
├── run.py                 # Entry point
└── requirements.txt
```

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and add your HuggingFace API token

3. Run:
   ```bash
   python run.py
   ```

4. Open http://localhost:8000

## How It Works

1. **Document Upload**: PDF is loaded and split into chunks
2. **Embedding**: Chunks are converted to vectors using sentence-transformers
3. **Storage**: Vectors are stored in ChromaDB
4. **Query**: User question is embedded and similar chunks are retrieved
5. **Answer**: LLM generates answer using retrieved context

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main page |
| `/process-document` | POST | Upload PDF |
| `/process-message` | POST | Ask question |
| `/status` | GET | Service status |
| `/clear-history` | POST | Reset chat |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `HUGGINGFACE_API_TOKEN` | HuggingFace API key |
| `LLM_MODEL_ID` | Model to use (default: falcon-7b-instruct) |
| `FLASK_PORT` | Server port (default: 8000) |

