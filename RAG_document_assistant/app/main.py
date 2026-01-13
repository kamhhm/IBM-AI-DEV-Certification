"""Flask application for RAG for Tech Docs."""

import logging
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

from app.config import config
from app.services import rag

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)
CORS(app)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max upload

# Log warning if API token not set
if not config.huggingface_api_token:
    logger.warning("HUGGINGFACE_API_TOKEN not set. LLM calls will fail.")


@app.route("/")
def index():
    """Serve the main page."""
    return render_template("index.html")


@app.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})


@app.route("/process-message", methods=["POST"])
def process_message():
    """Process a user message and return AI response."""
    data = request.get_json()
    
    if not data or "userMessage" not in data:
        return jsonify({"error": "Missing userMessage"}), 400
    
    user_message = data["userMessage"].strip()
    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400
    
    try:
        result = rag.query(user_message)
        return jsonify({"botResponse": result["answer"]})
    except RuntimeError as e:
        return jsonify({"botResponse": str(e)})
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/process-document", methods=["POST"])
def process_document():
    """Upload and process a PDF document."""
    if "file" not in request.files:
        return jsonify({"botResponse": "No file uploaded."}), 400
    
    file = request.files["file"]
    
    if file.filename == "":
        return jsonify({"botResponse": "No file selected."}), 400
    
    if not file.filename.lower().endswith(".pdf"):
        return jsonify({"botResponse": "Only PDF files are supported."}), 400
    
    try:
        # Save file
        filename = secure_filename(file.filename)
        upload_path = Path(config.upload_folder)
        upload_path.mkdir(exist_ok=True)
        file_path = upload_path / filename
        file.save(str(file_path))
        
        # Process document
        result = rag.process_document(str(file_path))
        
        return jsonify({
            "botResponse": f"Processed '{result['document']}' ({result['pages']} pages, {result['chunks']} chunks). You can now ask questions!"
        })
    except Exception as e:
        logger.error(f"Error processing document: {e}")
        return jsonify({"botResponse": f"Error: {str(e)}"}), 500


@app.route("/status")
def status():
    """Get RAG service status."""
    return jsonify(rag.get_status())


@app.route("/clear-history", methods=["POST"])
def clear_history():
    """Clear chat history."""
    rag.clear_history()
    return jsonify({"status": "cleared"})


if __name__ == "__main__":
    app.run(debug=config.flask_debug, port=config.flask_port, host=config.flask_host)
