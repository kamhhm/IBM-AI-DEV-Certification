"""
Flask Web Application for Sentiment Analysis
Executing this function initiates the application of sentiment
analysis to be executed over the Flask channel and deployed on
localhost:5000.
"""

import json

from dotenv import load_dotenv
from flask import Flask, render_template, request

from practice_project.SentimentAnalysis.sentiment_analysis import sentiment_analyzer

# Load environment variables from .env file
load_dotenv()

# Initiate the Flask app
app = Flask(__name__)


def format_sentiment_response(response_dict):
    """
    Formats the sentiment analysis response into an HTML display.

    Args:
        response_dict (dict): Dictionary containing 'label' and 'score', or 'error'

    Returns:
        str: Formatted HTML string
    """
    # Check for error first
    if 'error' in response_dict:
        return f"""
        <div class="alert alert-danger" role="alert">
            <strong>Error:</strong> {response_dict['error']}
        </div>
        """

    # Extract sentiment label and score from the response dictionary
    sentiment_label = response_dict.get('label')
    confidence_score = response_dict.get('score')

    # If we have sentiment info, format it for display
    if sentiment_label and confidence_score is not None:
        # Map sentiment labels to Bootstrap color classes
        sentiment_colors = {
            'positive': 'success',
            'negative': 'danger',
            'neutral': 'secondary',
            'POSITIVE': 'success',
            'NEGATIVE': 'danger',
            'NEUTRAL': 'secondary'
        }

        color_class = sentiment_colors.get(sentiment_label.upper(), 'info')
        if confidence_score <= 1:
            confidence_percent = round(confidence_score * 100, 2)
        else:
            confidence_percent = round(confidence_score, 2)
        return f"""
        <div class="card border-{color_class} mb-3">
            <div class="card-header bg-{color_class} text-white">
                <h4 class="mb-0">Sentiment: {sentiment_label.upper()}</h4>
            </div>
            <div class="card-body">
                <h5 class="card-title">Confidence Score</h5>
                <div class="progress mb-3" style="height: 30px;">
                    <div class="progress-bar bg-{color_class}" role="progressbar" 
                         style="width: {confidence_percent}%" 
                         aria-valuenow="{confidence_percent}" 
                         aria-valuemin="0" 
                         aria-valuemax="100">
                        {confidence_percent}%
                    </div>
                </div>
                <p class="card-text"><small class="text-muted">Raw score: {confidence_score}</small></p>
            </div>
        </div>
        <details class="mt-3">
            <summary style="cursor: pointer; color: #6c757d;">View Raw Response</summary>
            <pre class="mt-2" style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto;">{json.dumps(response_dict, indent=2)}</pre>
        </details>
        """

    # Fallback: show formatted response
    return f"""
    <div class="alert alert-info" role="alert">
        <strong>Response received:</strong>
    </div>
    <pre style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto;">{json.dumps(response_dict, indent=2)}</pre>
    """


@app.route("/sentimentAnalyzer")
def sent_analyzer():
    """
    This code receives the text from the HTML interface and
    runs sentiment analysis over it using sentiment_analyzer()
    function. The output returned shows the label and its confidence
    score for the provided text.
    """
    # Retrieve the text to analyze from the request arguments
    text_to_analyze = request.args.get('textToAnalyze')

    if not text_to_analyze:
        return json.dumps({"error": "No text provided"})

    # Pass the text to the sentiment_analyzer function and store the response
    response = sentiment_analyzer(text_to_analyze)

    # Check if the response contains an error
    if 'error' in response:
        return format_sentiment_response(response)

    # Extract the label from the response
    label = response.get('label')

    # Check if the label is None, indicating an error or invalid input
    if label is None:
        return "Invalid input! Try again."

    # Format and return the response with sentiment information
    return format_sentiment_response(response)


@app.route("/")
def render_index_page():
    """
    This function initiates the rendering of the main application
    page over the Flask channel
    """
    return render_template('index.html')


if __name__ == "__main__":
    # This function executes the flask app and deploys it on localhost:5001
    app.run(host="0.0.0.0", port=5001, debug=True)
