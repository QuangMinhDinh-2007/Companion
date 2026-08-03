from unittest.mock import patch, MagicMock
import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.testclient import TestClient

from app.core.auth import get_current_user_id
from app.main import app


def _cred(token="fake-token"):
    return HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)


@patch("app.core.auth.get_db")
def test_valid_token_returns_user_id(mock_get_db):
    fake = MagicMock()
    fake.user.id = "11111111-1111-1111-1111-111111111111"
    mock_get_db.return_value.auth.get_user.return_value = fake

    assert get_current_user_id(_cred()) == "11111111-1111-1111-1111-111111111111"


@patch("app.core.auth.get_db")
def test_invalid_token_raises_401(mock_get_db):
    mock_get_db.return_value.auth.get_user.side_effect = Exception("bad token")
    with pytest.raises(HTTPException) as exc:
        get_current_user_id(_cred("garbage"))
    assert exc.value.status_code == 401


@patch("app.core.auth.get_db")
def test_verified_but_no_user_raises_401(mock_get_db):
    resp = MagicMock()
    resp.user = None                      # token decoded, but no user attached
    mock_get_db.return_value.auth.get_user.return_value = resp
    with pytest.raises(HTTPException) as exc:
        get_current_user_id(_cred())
    assert exc.value.status_code == 401


def test_chat_endpoint_rejects_missing_token():
    client = TestClient(app)
    r = client.post("/api/chat", json={"message": "hi"})
    # HTTPBearer blocks before the handler runs, so Claude/DB are never touched.
    assert r.status_code in (401, 403)