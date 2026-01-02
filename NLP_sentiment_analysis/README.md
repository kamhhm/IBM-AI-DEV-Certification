# Sentiment Analysis Web Application

A web-based sentiment analysis app built with Watson NLP API and Flask. BERT model for the NLP API. Python Flask for web deployement. JavaScript for front end functionaility. 

## Main Learnings
- Real-time sentiment analysis using Watson NLP BERT model
- Bootstrap-styled UI for text input and sentiment analysis
- Flask backend with dedicated endpoints for sentiment analysis
- Robust error handling for API failures and invalid inputs

## Potential Future Improvements

- [ ] Implement caching for frequently analyzed texts
- [ ] Add support for batch sentiment analysis
- [ ] Add visualization of sentiment scores
- [ ] Support for multiple languages


## Project Structure

```
zzrjt-practice-project-emb-ai/
├── practice_project/
│   ├── SentimentAnalysis/
│   │   ├── __init__.py
│   │   └── sentiment_analysis.py    # Core sentiment analysis module
│   └── test_sentiment_analysis.py   # Unit tests
├── templates/
│   └── index.html                   # Web interface template
├── static/
│   └── mywebscript.js               # Frontend JavaScript
├── flask_server.py                   # Flask application server
├── requirements.txt                  # Python dependencies
├── LICENSE                           # License file
├── .gitignore                        # Git ignore rules
└── README.md                         # Project documentation
```


## Usage

### Running the Web Application

1. Install dependencies (if not already installed):
```bash
pip install -r requirements.txt
```

2. Configure API credentials (optional for testing):
Create a `.env` file in the project root:
```env
WATSON_API_KEY=your_api_key_here
WATSON_API_URL=https://sn-watson-sentiment-bert.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/SentimentPredict
```

3. Start the Flask server:
```bash
python3 flask_server.py
```

4. Open your browser and navigate to:
```
http://localhost:5001
```

Note: Port 5001 is used because port 5000 is typically occupied by AirPlay Receiver on macOS.

5. Enter text in the input field and click "Run Sentiment Analysis" to see the results.

### Using the Sentiment Analysis Module Directly

You can also use the sentiment analysis function directly in a Python shell:

```python
from practice_project.SentimentAnalysis.sentiment_analysis import sentiment_analyzer

# Make sure WATSON_API_KEY is set in your environment or .env file
result = sentiment_analyzer("I am happy today")
print(result)
```



