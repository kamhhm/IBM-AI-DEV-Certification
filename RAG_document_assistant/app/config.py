"""Configuration loaded from environment variables."""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """App configuration from environment variables."""
    
    # HuggingFace
    huggingface_api_token = os.getenv("HUGGINGFACE_API_TOKEN", "")
    
    # Models
    llm_model_id = os.getenv("LLM_MODEL_ID", "tiiuae/falcon-7b-instruct")
    embedding_model_id = os.getenv("EMBEDDING_MODEL_ID", "sentence-transformers/all-MiniLM-L6-v2")
    
    # LLM parameters
    llm_temperature = float(os.getenv("LLM_TEMPERATURE", "0.1"))
    llm_max_new_tokens = int(os.getenv("LLM_MAX_NEW_TOKENS", "600"))
    
    # RAG settings
    chunk_size = int(os.getenv("CHUNK_SIZE", "1024"))
    chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "64"))
    retriever_k = int(os.getenv("RETRIEVER_K", "6"))
    
    # Flask
    flask_debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    flask_port = int(os.getenv("FLASK_PORT", "8000"))
    flask_host = os.getenv("FLASK_HOST", "0.0.0.0")
    
    # Paths
    upload_folder = os.getenv("UPLOAD_FOLDER", "uploads")


config = Config()
