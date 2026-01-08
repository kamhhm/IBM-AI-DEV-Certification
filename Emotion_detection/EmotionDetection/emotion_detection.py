"""
Emotion Detection module using Watson NLP library.
"""
import requests


def emotion_detector(text_to_analyse):
    """
    Analyze text and return emotion scores using Watson NLP.

    Args:
        text_to_analyse: The text string to analyze

    Returns:
        Dictionary with emotion scores and dominant emotion.
        Returns None values if input is blank (status 400).
    """
    url = ('https://sn-watson-emotion.labs.skills.network'
           '/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict')

    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }

    input_json = {"raw_document": {"text": text_to_analyse}}

    response = requests.post(url, json=input_json, headers=headers, timeout=10)

    if response.status_code == 400:
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    formatted_response = response.json()
    emotions = formatted_response['emotionPredictions'][0]['emotion']

    anger_score = emotions['anger']
    disgust_score = emotions['disgust']
    fear_score = emotions['fear']
    joy_score = emotions['joy']
    sadness_score = emotions['sadness']

    emotion_scores = {
        'anger': anger_score,
        'disgust': disgust_score,
        'fear': fear_score,
        'joy': joy_score,
        'sadness': sadness_score
    }
    dominant_emotion = max(emotion_scores, key=emotion_scores.get)

    return {
        'anger': anger_score,
        'disgust': disgust_score,
        'fear': fear_score,
        'joy': joy_score,
        'sadness': sadness_score,
        'dominant_emotion': dominant_emotion
    }
