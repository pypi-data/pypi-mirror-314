from pathlib import Path
from unittest.mock import Mock, patch
from consilio.assemble import assemble, xml_to_markdown

# Test data
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


@patch("consilio.assemble.query_claude")
def test_assemble(mock_query, mock_doc, mock_context):
    # Configure mock
    mock_response = Mock()
    mock_response.content = SAMPLE_XML
    mock_query.return_value = mock_response

    # Call function
    result = assemble(mock_doc, mock_context)

    # Verify result
    assert result.startswith("<perspectives>")
    assert "Test Perspective" in result

    # Verify Claude was called correctly
    mock_query.assert_called_once()
    call_args = mock_query.call_args[1]
    assert "Test decision" in call_args["user_prompt"]
    assert mock_context["domain"] in call_args["system_prompt"]
    assert call_args["temperature"] == 0.8


def test_xml_to_markdown():
    markdown = xml_to_markdown(SAMPLE_XML)

    # Verify markdown formatting
    assert "## Test Perspective\n" in markdown
    assert "*Test relevance*" in markdown
    assert "- Test question 1?" in markdown
    assert "- Test question 2?" in markdown

@patch("consilio.assemble.query_claude")
def test_assemble_main(mock_query, mock_doc, mock_context, monkeypatch):
    # Mock Path.parent and Path.__truediv__
    mock_path = Mock()
    mock_path.parent = mock_path
    mock_path.__truediv__ = lambda self, x: mock_path
    monkeypatch.setattr(Path, "__new__", lambda cls, *args, **kwargs: mock_path)
    
    # Configure mock response
    mock_response = Mock()
    mock_response.content = SAMPLE_XML
    mock_query.return_value = mock_response
    
    # Mock read_text
    mock_path.read_text = lambda: "Test Content"
    
    # Run the main block
    with patch("consilio.assemble.Path") as mock_path_cls:
        mock_path_cls.return_value = mock_path
        import consilio.assemble
        if hasattr(consilio.assemble, "__main__"):
            exec(consilio.assemble.__main__)
