
import pytest
from unittest.mock import patch, MagicMock
from chineseroom.gemini_client import GeminiClient


@pytest.fixture
def dummy_api_key(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "dummy_key")
    return "dummy_key"


@pytest.fixture
def mock_generative_model():
    with patch("google.generativeai.GenerativeModel") as mock_model_cls:
        mock_model = MagicMock()
        mock_model.generate_content.return_value.text = "mocked response"
        mock_model_cls.return_value = mock_model
        yield mock_model


def test_init_with_env(monkeypatch, dummy_api_key, mock_generative_model):
    client = GeminiClient()
    assert client.api_key == "dummy_key"


def test_init_with_arg(mock_generative_model):
    client = GeminiClient(api_key="another_key")
    assert client.api_key == "another_key"


def test_ask_returns_text(monkeypatch, dummy_api_key, mock_generative_model):
    client = GeminiClient()
    result = client.ask("hello")
    assert result == "mocked response"


def test_ask_handles_exception(monkeypatch, dummy_api_key):
    with patch("google.generativeai.GenerativeModel") as mock_model_cls:
        mock_model = MagicMock()
        mock_model.generate_content.side_effect = Exception("API error")
        mock_model_cls.return_value = mock_model
        client = GeminiClient()
        with pytest.raises(RuntimeError, match="Gemini API error: API error"):
            client.ask("fail")
