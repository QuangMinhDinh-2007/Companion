# tests/test_chat.py
from unittest.mock import patch, MagicMock
from app.core.companion import get_response

@patch("app.core.companion.client")
def test_get_response_returns_reply(mock_client):
    fake = MagicMock()
    fake.content = [MagicMock(text="I hear you. That sounds hard.")]
    mock_client.messages.create.return_value = fake

    result = get_response(
        user_message="I feel alone",
        chat_history=[],
        emotion="sad",
    )

    assert result == "I hear you. That sounds hard."