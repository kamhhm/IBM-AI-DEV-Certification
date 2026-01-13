#!/usr/bin/env python3
"""Entry point for the RAG for Tech Docs application."""

from app.main import app
from app.config import config

if __name__ == "__main__":
    print(f"Starting server at http://{config.flask_host}:{config.flask_port}")
    app.run(
        debug=config.flask_debug,
        port=config.flask_port,
        host=config.flask_host
    )
