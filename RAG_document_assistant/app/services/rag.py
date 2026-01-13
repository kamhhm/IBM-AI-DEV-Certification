"""RAG pipeline for document processing and question answering."""

import os
from pathlib import Path
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

from app.config import config
from app.services import llm as llm_service

# Global state
qa_chain = None
chat_history = []
vector_store = None
loaded_documents = []


def process_document(document_path):
    """
    Process a PDF document for RAG.
    
    Args:
        document_path: Path to the PDF file
        
    Returns:
        dict with processing results
    """
    global qa_chain, vector_store, loaded_documents
    
    # Make sure models are initialized
    if llm_service.llm is None:
        llm_service.init_models()
    
    # Load PDF
    loader = PyPDFLoader(document_path)
    documents = loader.load()
    
    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.chunk_size,
        chunk_overlap=config.chunk_overlap
    )
    chunks = text_splitter.split_documents(documents)
    
    # Create/update vector store
    if vector_store is None:
        vector_store = Chroma.from_documents(chunks, embedding=llm_service.embeddings)
    else:
        vector_store.add_documents(chunks)
    
    # Create QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm_service.llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={"k": config.retriever_k, "lambda_mult": 0.25}
        ),
        return_source_documents=False,
        input_key="question"
    )
    
    loaded_documents.append(Path(document_path).name)
    
    return {
        "status": "success",
        "document": Path(document_path).name,
        "pages": len(documents),
        "chunks": len(chunks)
    }


def query(question):
    """
    Query the loaded documents.
    
    Args:
        question: User's question
        
    Returns:
        dict with the answer
    """
    global chat_history
    
    if qa_chain is None:
        raise RuntimeError("No documents loaded. Please upload a document first.")
    
    # Get answer from chain
    result = qa_chain.invoke({
        "question": question,
        "chat_history": chat_history
    })
    
    answer = result["result"]
    
    # Update chat history
    chat_history.append((question, answer))
    
    return {"answer": answer}


def clear_history():
    """Clear the chat history."""
    global chat_history
    chat_history = []


def get_status():
    """Get current status of the RAG service."""
    return {
        "documents_loaded": loaded_documents,
        "chat_history_length": len(chat_history),
        "ready": qa_chain is not None
    }
