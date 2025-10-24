import uuid
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from freezegun import freeze_time

from app.infrastructure.db import db_models
from app.infrastructure.db.sqlite import get_mock_session
from app.main import app

client = TestClient(app)


@pytest.mark.parametrize(
    "username, password, status_code, json_response",
    [
        pytest.param(
            "sh-okada",
            "Password123",
            200,
            {
                "id": "5e3868cd-3ec0-4f86-9a94-84363c64da29",
                "username": "sh-okada",
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1ZTM4NjhjZC0zZWMwLTRmODYtOWE5NC04NDM2M2M2NGRhMjkiLCJleHAiOjE3NTMyMzA2MDB9.cTPZJnsl44nXmY9dfDS7mOc1s11mjCenmdy14FH_wzg",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1ZTM4NjhjZC0zZWMwLTRmODYtOWE5NC04NDM2M2M2NGRhMjkiLCJleHAiOjE3NjEwMDQ4MDB9.SeDvySQ7qXWfTsuMOTQYCgzwMGAGg33ptDnRTxrC85c",
            },
            id="ユーザー名とパスワードの組み合わせが正しい場合、ログインできること",
        ),
        pytest.param(
            "bad-user",
            "Password123",
            400,
            {"detail": "Incorrect username or password."},
            id="ユーザー名が間違っている場合、ログインできないこと",
        ),
        pytest.param(
            "sh-okada",
            "BadPassword123",
            400,
            {"detail": "Incorrect username or password."},
            id="パスワードが間違っている場合、ログインできないこと",
        ),
    ],
)
def test_レスポンス(
    username: str, password: str, status_code: int, json_response: dict
):
    user = db_models.User(
        id=uuid.UUID("5e3868cd-3ec0-4f86-9a94-84363c64da29"),
        name="sh-okada",
        password="$2b$12$ypi5a45bRgKPo4ZJk2IvQeqKJLlfpmGGwL9Pu9i/rEs2Pa0y7SywS",
    )

    session = next(get_mock_session())
    session.add(user)
    session.commit()

    with freeze_time(datetime(2025, 7, 23, 0, 0, 0)):
        response = client.post(
            "/api/auth/login", data={"username": username, "password": password}
        )

    assert response.status_code == status_code
    assert response.json() == json_response
