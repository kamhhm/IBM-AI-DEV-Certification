"""
Sentiment Analysis Module
This module provides functionality to analyze sentiment of text using Watson NLP API.
"""

import requests
import json
import os


def sentiment_analyzer(text_to_analyse):
    """
    Analyzes the sentiment of the given text using Watson NLP API.
    
    Args:
        text_to_analyse (str): The text to analyze for sentiment
        
    Returns:
        dict: Dictionary containing sentiment label and score, or error message
        
    Example:
        >>> result = sentiment_analyzer("I am happy today")
        >>> print(result)
        {'label': 'POSITIVE', 'score': 0.95}
    """
    # Get API credentials from environment variables
    api_key = os.getenv('WATSON_API_KEY')
    api_url = os.getenv('WATSON_API_URL', 
                       'https://sn-watson-sentiment-bert.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/SentimentPredict')
    
    # Validate API key is set
    if not api_key:
        return {'error': 'WATSON_API_KEY environment variable is not set. Please configure your API credentials.'}
    
    # Constructing the request payload in the expected format
    myobj = { "raw_document": { "text": text_to_analyse } }

    # Headers with API key authentication and model ID
    headers = {
        "grpc-metadata-mm-model-id": "sentiment_aggregated-bert-workflow_lang_multi_stock",
        "Authorization": f"Bearer {api_key}"
    }

    try:
        # Sending a POST request to the sentiment analysis API
        response = requests.post(api_url, json=myobj, headers=headers, timeout=30)
        
        # Parse the response from the API
        formatted_response = json.loads(response.text)
        
        # If the response status code is 200, extract the label and score from the response
        if response.status_code == 200:
            label = formatted_response['documentSentiment']['label']
            score = formatted_response['documentSentiment']['score']
        # If the response status code is 500, set label and score to None
        elif response.status_code == 500:
            label = None
            score = None
        else:
            # For other error status codes, raise an exception
            response.raise_for_status()
            label = None
            score = None
        
        # Return the label and score in a dictionary
        return {'label': label, 'score': score}
    except requests.exceptions.RequestException as e:
        return {'error': f"Failed to analyze sentiment: {str(e)}"}
    except (KeyError, json.JSONDecodeError) as e:
        return {'error': f"Failed to parse response: {str(e)}"}


if __name__ == "__main__":
    # Example usage
    test_texts = [
        "I am happy today",
        "I am sad today",
        "I am excited about this project"
    ]
    
    for text in test_texts:
        result = sentiment_analyzer(text)
        print(f"Text: {text}")
        print(f"Label: {result.get('label', 'N/A')}")
        print(f"Score: {result.get('score', 'N/A')}")
        print()