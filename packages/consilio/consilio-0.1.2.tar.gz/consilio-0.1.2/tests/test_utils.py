import yaml
from pathlib import Path
from unittest.mock import Mock, patch
from consilio.utils import (
    escape_xml_string, ClaudeResponse, load_context,
    PromptTemplate, render_prompt, save_last_doc_path,
    load_last_doc_path, create_decision_dir, query_claude,
    save_interaction, generate_interaction_filename
)

def test_generate_interaction_filename(freezer):
    # Freeze time to 2024-01-01 12:34:56
    freezer.move_to("2024-01-01 12:34:56")

    # Test basic filename generation
    filename = generate_interaction_filename("observe")
    assert filename == "240101_123456-observe.md"

    # Test filename with perspective
    filename = generate_interaction_filename("consult", "Test Perspective")
    assert filename == "240101_123456-consult_Test_Perspective.md"

def test_escape_xml_string():
    # Test basic XML escaping
    assert escape_xml_string("test & test") == "test &amp; test"
    assert escape_xml_string(" test ") == "test"  # Tests strip()

def test_claude_response():
    # Test ClaudeResponse dataclass
    raw_response = {"content": "test", "other": "data"}
    response = ClaudeResponse(content="test", raw=raw_response)
    assert response.content == "test"
    assert response.raw == raw_response

def test_load_context_from_file(tmp_path):
    # Test loading context from yaml file
    config_path = tmp_path / ".consilio.yml"
    config_data = {
        "domain": "test domain",
        "perspective": "test perspective",
        "user_role": "test role"
    }
    with open(config_path, "w") as f:
        yaml.dump(config_data, f)
    
    context = load_context(config_path)
    assert context.domain == "test domain"
    assert context.perspective == "test perspective"
    assert context.user_role == "test role"

@patch('builtins.input')
def test_load_context_from_input(mock_input):
    # Test loading context from user input
    mock_input.side_effect = [
        "test domain",
        "test role",
        "test perspective",
        "n"  # Don't save
    ]
    context = load_context(Path("nonexistent.yml"))
    assert context.domain == "test domain"
    assert context.perspective == "test perspective"
    assert context.user_role == "test role"

def test_prompt_template():
    # Test PromptTemplate loading and rendering
    template = PromptTemplate(
        system="Hello {{domain}}",
        user="Hi {{user_role}}"
    )
    context = {"domain": "test", "user_role": "tester"}
    rendered_system = render_prompt(template.system, context)
    rendered_user = render_prompt(template.user, context)
    assert rendered_system == "Hello test"
    assert rendered_user == "Hi tester"

def test_save_and_load_last_doc_path(tmp_path):
    # Test saving and loading last document path
    test_path = tmp_path / "test.md"
    save_last_doc_path(test_path)
    loaded_path = load_last_doc_path()
    assert str(loaded_path) == str(test_path)

def test_create_decision_dir():
    # Test creating decision directory
    decision_dir = create_decision_dir("test_decision")
    assert decision_dir.exists()
    assert decision_dir.is_dir()
    assert decision_dir.name == "test_decision"


@patch('consilio.utils.anthropic.Anthropic')
def test_query_claude(mock_anthropic):
    # Test Claude API interaction
    mock_client = Mock()
    mock_response = Mock()
    mock_response.content = [Mock(type="text", text="test response")]
    mock_response.model_dump.return_value = {"content": [{"type": "text", "text": "test response"}]}
    mock_client.messages.create.return_value = mock_response
    mock_anthropic.return_value = mock_client

    response = query_claude(
        user_prompt="test prompt",
        system_prompt="test system",
        assistant="test assistant",
        temperature=0.8
    )
    
    assert response.content == "test response"
    mock_client.messages.create.assert_called_once()

def test_save_interaction_decorator():
    # Test the save_interaction decorator
    @save_interaction("test")
    def test_func(doc: Path, *args, **kwargs):
        return "test result"
    
    doc_path = Path("test.md")
    result = test_func(doc_path)
    assert result == "test result"
