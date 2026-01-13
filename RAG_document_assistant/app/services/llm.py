"""LLM and embeddings initialization using HuggingFace."""

import os
import torch
from langchain_community.llms import HuggingFaceHub
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from app.config import config

# Determine device (GPU if available, otherwise CPU)
DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"

# These will be initialized when init_models() is called
llm = None
embeddings = None


def init_models():
    """Initialize the LLM and embeddings models."""
    global llm, embeddings
    
    # Set HuggingFace API token
    if config.huggingface_api_token:
        os.environ["HUGGINGFACEHUB_API_TOKEN"] = config.huggingface_api_token
    
    # Initialize LLM
    llm = HuggingFaceHub(
        repo_id=config.llm_model_id,
        model_kwargs={
            "temperature": config.llm_temperature,
            "max_new_tokens": config.llm_max_new_tokens,
            "max_length": config.llm_max_new_tokens,
        }
    )
    
    # Initialize embeddings
    embeddings = HuggingFaceInstructEmbeddings(
        model_name=config.embedding_model_id,
        model_kwargs={"device": DEVICE}
    )
    
    print(f"Models initialized (device: {DEVICE})")
