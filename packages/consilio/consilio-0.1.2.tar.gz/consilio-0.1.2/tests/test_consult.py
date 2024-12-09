from pathlib import Path
from unittest.mock import Mock, patch
from consilio.consult import consult, get_perspective_opinion

SAMPLE_XML = """
<perspectives>
    <perspective>
        <title>Test Perspective</title>
        <relevance>Test relevance</relevance>
        <questions>
            <question>Test question 1?</question>
            <question>Test question 2?</question>
        </questions>
    </perspective>
</perspectives>
"""

SAMPLE_OPINION = "This is a test opinion from the perspective."

@patch('consilio.consult.query_claude')
def test_get_perspective_opinion(mock_query, mock_doc, mock_context):
    # Configure mock
    mock_response = Mock()
    mock_response.content = SAMPLE_OPINION
    mock_query.return_value = mock_response
    
    # Call function
    result = get_perspective_opinion(
        doc=mock_doc,
        title="Test Perspective",
        user_prompt="test prompt",
        assistant_prefix="test prefix",
        perspective_title="Test Perspective"
    )
    
    # Verify result
    assert result == SAMPLE_OPINION
    
    # Verify Claude was called correctly
    mock_query.assert_called_once()
    call_args = mock_query.call_args[1]
    assert call_args["user_prompt"] == "test prompt"
    assert call_args["assistant"] == "test prefix"
    assert call_args["temperature"] == 0.8

@patch('consilio.consult.query_claude')
def test_consult(mock_query, mock_doc, mock_context):
    # Configure mock
    mock_response = Mock()
    mock_response.content = "Test opinion content"
    mock_query.return_value = mock_response
    
    result = consult(mock_doc, SAMPLE_XML, mock_context)
    
    # Verify result structure
    assert result.startswith("<opinions>")
    assert result.endswith("</opinions>")
    assert "<opinion>" in result
    
    # Verify Claude was called correctly
    assert mock_query.call_count == 1  # One call per perspective in SAMPLE_XML

@patch('consilio.consult.query_claude')
def test_consult_main(mock_query, mock_doc, mock_context, monkeypatch):
    # Mock Path.parent and Path.__truediv__
    mock_path = Mock()
    mock_path.parent = mock_path
    mock_path.__truediv__ = lambda self, x: mock_path
    monkeypatch.setattr(Path, "__new__", lambda cls, *args, **kwargs: mock_path)
    
    # Configure mock response
    mock_response = Mock()
    mock_response.content = "Test opinion content"
    mock_query.return_value = mock_response
    
    # Mock read_text
    mock_path.read_text = lambda: "Test Content"
    
    # Run the main block
    with patch("consilio.consult.Path") as mock_path_cls:
        mock_path_cls.return_value = mock_path
        import consilio.consult
        if hasattr(consilio.consult, "__main__"):
            exec(consilio.consult.__main__)
