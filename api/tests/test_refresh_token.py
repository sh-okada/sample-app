import uuid
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from freezegun import freeze_time

from app.infrastructure.db import db_models
from app.infrastructure.db.sqlite import get_mock_session
from app.main import app
from tests.conftest import expired_refresh_token, valid_refresh_token

client = TestClient(app)


@pytest.mark.parametrize(
    "request_body, status_code, json_response",
    [
        pytest.param(
            {
                "refresh_token": valid_refresh_token(
                    "5e3868cd-3ec0-4f86-9a94-84363c64da29"
                ),
            },
            200,
            {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1ZTM4NjhjZC0zZWMwLTRmODYtOWE5NC04NDM2M2M2NGRhMjkiLCJleHAiOjE3NTMyMjk3MDB9.EX2iOXELnlMLgTsOk2CBz9fp8wQ8BHc9DiehrSLeO_w",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1ZTM4NjhjZC0zZWMwLTRmODYtOWE5NC04NDM2M2M2NGRhMjkiLCJleHAiOjE3NjEwMDQ4MDB9.SeDvySQ7qXWfTsuMOTQYCgzwMGAGg33ptDnRTxrC85c",
            },
            id="アクセストークンとリフレッシュトークンが新しく発行されること",
        ),
        pytest.param(
            {
                "refresh_token": valid_refresh_token(
                    "d105b272-67b3-4ff8-b07b-15764c4ea886"
                ),
            },
            401,
            {
                "detail": "User not found.",
            },
            id="存在しないユーザーIDのリフレッシュトークンではトークンを発行できないこと",
        ),
        pytest.param(
            {
                "refresh_token": expired_refresh_token(
                    "5e3868cd-3ec0-4f86-9a94-84363c64da29"
                ),
            },
            401,
            {
                "detail": "Refresh token has expired.",
            },
            id="有効期限が切れているリフレッシュトークンではトークンを発行できないこと",
        ),
    ],
)
def test_レスポンス(request_body: dict, status_code: int, json_response: dict):
    user = db_models.User(
        id=uuid.UUID("5e3868cd-3ec0-4f86-9a94-84363c64da29"),
        name="sh-okada",
        password="$2b$12$ypi5a45bRgKPo4ZJk2IvQeqKJLlfpmGGwL9Pu9i/rEs2Pa0y7SywS",
    )

    session = next(get_mock_session())
    session.add(user)
    session.commit()

    with freeze_time(datetime(2025, 7, 23, 0, 0, 0)):
        response = client.post("/api/auth/tokens/refresh", json=request_body)

    assert response.status_code == status_code
    assert response.json() == json_response
