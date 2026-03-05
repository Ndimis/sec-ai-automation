from unittest.mock import patch, MagicMock
from summarizer import IncidentSummarizer

@patch('summarizer.client.chat.completions.create')
def test_api_call_logic(mock_create):
    # Mock a successful API response
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Sample Summary"))]
    mock_create.return_value = mock_response
    
    summarizer = IncidentSummarizer()
    result = summarizer.generate_summary({"test": "data"})
    
    assert result == "Sample Summary"
    assert mock_create.called