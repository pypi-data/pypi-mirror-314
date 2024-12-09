# tests/test_response_processor.py

# pylint: disable=redefined-outer-name

from unittest.mock import patch
import pytest
from openai_integration.response_processor import ResponseProcessor

@pytest.fixture
def response_processor():
    """Fixture to initialize ResponseProcessor."""
    return ResponseProcessor()

def test_process_response_valid_format(response_processor):
    """Test processing a valid commit message."""
    valid_message = "feature | frontend: Add new user profile page"
    result = response_processor.process_response(valid_message)
    assert result == valid_message

def test_process_response_invalid_format(response_processor):
    """Test processing an invalid commit message format."""
    invalid_message = "Fixed the API endpoint response"
    with patch('builtins.print') as mock_print:
        result = response_processor.process_response(invalid_message)
        assert result is None
        mock_print.assert_called_with("Response from GPT:\n", invalid_message)

def test_process_response_unknown_change_type(response_processor):
    """Test processing a commit message with an unknown change type."""
    unknown_type_message = "enhancement | UI: Add dark mode support"
    with patch('builtins.print') as mock_print:
        result = response_processor.process_response(unknown_type_message)
        assert result is None
        mock_print.assert_called_with("Response from GPT:\n", unknown_type_message)

def test_process_response_normalize_change_type(response_processor):
    """Test that certain change types are normalized correctly."""
    message = "feat | backend: Add logging"
    result = response_processor.process_response(message)
    assert result == "feature | backend: Add logging"

# def test_process_response_with_detailed_description(response_processor):
#     """Test processing a valid commit message with additional description."""
#     multiline_message = (
#         "fix | backend: Correct API response\n\nAdded error handling for unexpected inputs."
#     )
#     result = response_processor.process_response(multiline_message)
#     assert result == (
#         "bugfix | backend: Correct API response\n\nAdded error handling for unexpected inputs."
#     )

def test_process_response_case_sensitivity(response_processor):
    """Test that change types are case-sensitive."""
    message = "Fix | Backend: Correct issue"  # 'Fix' should be 'fix'
    result = response_processor.process_response(message)
    assert result == "bugfix | backend: Correct issue"

def test_process_response_valid_special_characters(response_processor):
    """Test processing a valid commit message containing special characters."""
    valid_message = "docs | README: Update README.md with new instructions!"
    result = response_processor.process_response(valid_message)
    assert result == "docs | readme: Update README.md with new instructions!"

def test_process_response_missing_impact_area(response_processor):
    """Test processing a commit message missing the impact area."""
    missing_impact_message = "fix | : Correct API response"
    with patch("builtins.print") as mock_print:
        result = response_processor.process_response(missing_impact_message)
        assert result is None
        mock_print.assert_called_with("Response from GPT:\n", missing_impact_message)

# def test_process_response_extra_sections(response_processor):
#     """Test processing a commit message with extra sections."""
#     extra_section_message = "fix | backend: Correct API response | urgent"
#     with patch("builtins.print") as mock_print:
#         result = response_processor.process_response(extra_section_message)
#         assert result is None
#         mock_print.assert_called_with("Response from GPT:\n", extra_section_message)
