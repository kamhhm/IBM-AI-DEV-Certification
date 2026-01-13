# RAG Document Assistant

A tool to help me (and devs) to accurately query and learn technical documentation faster.

Built with Flask on the backend, using LangChain to orchestrate the RAG pipeline. Documents are embedded using HuggingFace's sentence-transformers and stored in ChromaDB for semantic search. The LLM (Falcon-7B via HuggingFace) generates answers based on retrieved context.

## How It Works

1. **Document Upload**: PDF is loaded and split into chunks
2. **Embedding**: Chunks are converted to vectors using sentence-transformers
3. **Storage**: Vectors are stored in ChromaDB
4. **Query**: User question is embedded and similar chunks are retrieved
5. **Answer**: LLM generates answer using retrieved context


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

