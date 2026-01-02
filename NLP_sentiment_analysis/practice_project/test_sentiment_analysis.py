import unittest
import os
from practice_project.SentimentAnalysis.sentiment_analysis import sentiment_analyzer


class TestSentimentAnalyzer(unittest.TestCase):
    """Test cases for the sentiment_analyzer function."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Check if API key is set, skip tests if not available
        self.api_key = os.getenv('WATSON_API_KEY')
        if not self.api_key:
            self.skipTest("WATSON_API_KEY not set. Skipping API-dependent tests.")
    
    def test_sentiment_analyzer_positive(self):
        """Test case for positive sentiment."""
        result = sentiment_analyzer('I love this project')
        self.assertIn('label', result)
        self.assertIn('score', result)
        # Watson API returns 'POSITIVE', 'NEGATIVE', or 'NEUTRAL' (not 'SENT_POSITIVE')
        self.assertIn(result['label'].upper(), ['POSITIVE', 'SENT_POSITIVE'])
        self.assertIsInstance(result['score'], (int, float))
        self.assertGreaterEqual(result['score'], 0)
        self.assertLessEqual(result['score'], 1)
    
    def test_sentiment_analyzer_negative(self):
        """Test case for negative sentiment."""
        result = sentiment_analyzer('I hate this project')
        self.assertIn('label', result)
        self.assertIn('score', result)
        # Watson API returns 'POSITIVE', 'NEGATIVE', or 'NEUTRAL'
        self.assertIn(result['label'].upper(), ['NEGATIVE', 'SENT_NEGATIVE'])
        self.assertIsInstance(result['score'], (int, float))
        self.assertGreaterEqual(result['score'], 0)
        self.assertLessEqual(result['score'], 1)
    
    def test_sentiment_analyzer_neutral(self):
        """Test case for neutral sentiment."""
        result = sentiment_analyzer('I am neutral on this project')
        self.assertIn('label', result)
        self.assertIn('score', result)
        # Watson API returns 'POSITIVE', 'NEGATIVE', or 'NEUTRAL'
        self.assertIn(result['label'].upper(), ['NEUTRAL', 'SENT_NEUTRAL'])
        self.assertIsInstance(result['score'], (int, float))
        self.assertGreaterEqual(result['score'], 0)
        self.assertLessEqual(result['score'], 1)
    
    def test_sentiment_analyzer_empty_string(self):
        """Test case for empty string input."""
        result = sentiment_analyzer('')
        # Should handle empty string gracefully
        self.assertIsInstance(result, dict)
    
    def test_sentiment_analyzer_no_api_key(self):
        """Test case when API key is not set."""
        # Temporarily remove API key
        original_key = os.environ.get('WATSON_API_KEY')
        if 'WATSON_API_KEY' in os.environ:
            del os.environ['WATSON_API_KEY']
        
        result = sentiment_analyzer('test text')
        self.assertIn('error', result)
        
        # Restore API key
        if original_key:
            os.environ['WATSON_API_KEY'] = original_key


if __name__ == '__main__':
    unittest.main()