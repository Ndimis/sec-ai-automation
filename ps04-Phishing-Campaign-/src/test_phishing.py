import pytest
from phishing_engine import PhishingAnalyzer

def test_obvious_phishing():
    analyzer = PhishingAnalyzer()
    body = "Immediate action required: account suspended. Click now."
    result = analyzer.analyze_email(body)
    assert result["is_phish"] == True

def test_clean_email():
    analyzer = PhishingAnalyzer()
    body = "Hey, are we still meeting for lunch at the cafeteria at 12?"
    result = analyzer.analyze_email(body)
    assert result["is_phish"] == False

def test_confidence_threshold():
    analyzer = PhishingAnalyzer()
    # High similarity to a known template
    body = "Unauthorised login detected on your account. Update password now."
    result = analyzer.analyze_email(body)
    assert result["confidence"] > 0.5