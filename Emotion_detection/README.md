# Emotion Detection Web Application

A web-based emotion detection app built with Watson NLP API and Flask. Detects five emotions (joy, anger, sadness, fear, disgust) from text input and identifies the dominant emotion.

## Main Learnings
- Real-time emotion analysis using Watson NLP
- Flask backend with JSON API endpoints
- Error handling for blank inputs (status code 400)
- Unit testing with Python unittest
- Static code analysis with PyLint (10/10 score)

## Potential Future Improvements

- [ ] Add visualization charts for emotion scores
- [ ] Implement caching for repeated analyses
- [ ] Support for multiple languages
- [ ] Batch text analysis
- [ ] Export results to CSV/JSON


## Project Structure

```
final_project/
├── EmotionDetection/
│   ├── __init__.py
│   └── emotion_detection.py    # Core emotion detection module
├── templates/
│   └── index.html              # Web interface template
├── static/
│   └── mywebscript.js          # Frontend JavaScript
├── server.py                   # Flask application server
├── test_emotion_detection.py   # Unit tests
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```


## Usage

### Running the Web Application

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the Flask server:
```bash
python server.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

4. Enter text in the input field and click "Analyze" to see the results.

**Note:** The Watson NLP API endpoint (`sn-watson-emotion.labs.skills.network`) is only accessible within the IBM Skills Network lab environment.

### Using the Emotion Detection Module Directly

```python
from EmotionDetection.emotion_detection import emotion_detector

result = emotion_detector("I am so happy today")
print(result)
```
