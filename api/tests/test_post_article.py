import uuid
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from freezegun import freeze_time

from app.infrastructure.db import db_models
from app.infrastructure.db.sqlite import get_mock_session
from app.main import app
from tests.conftest import (
    expired_jwt_token,
    valid_jwt_token,
)

client = TestClient(app)


@pytest.fixture(autouse=True)
def before_each():
    user = db_models.User(
        id=uuid.UUID("caa93979-2256-42f0-8e83-55144674613b"),
        name="sh-okada",
        password="$2b$12$ypi5a45bRgKPo4ZJk2IvQeqKJLlfpmGGwL9Pu9i/rEs2Pa0y7SywS",
    )

    session = next(get_mock_session())
    session.add(user)
    session.commit()


@pytest.mark.parametrize(
    "headers, request_body, status_code, json_response",
    [
        pytest.param(
            {
                "Authorization": f"Bearer {valid_jwt_token('caa93979-2256-42f0-8e83-55144674613b')}"
            },
            {"title": "タイトル", "text": "テキスト"},
            201,
            {"detail": "Article created successfully."},
            id="記事を投稿できること",
        ),
        pytest.param(
            None,
            {"title": "タイトル", "text": "テキスト"},
            401,
            {"detail": "Not authenticated"},
            id="JWTがない状態で記事を投稿できないこと",
        ),
        pytest.param(
            {"Authorization": "Bearer invalid-token"},
            {"title": "タイトル", "text": "テキスト"},
            401,
            {"detail": "Invalid token."},
            id="不正なJWTでは記事を投稿できないこと",
        ),
        pytest.param(
            {
                "Authorization": f"Bearer {valid_jwt_token('407a9844-da17-4b58-b60c-500d35d2e45a')}"
            },
            {"title": "タイトル", "text": "テキスト"},
            401,
            {"detail": "User not found."},
            id="存在しないユーザーのJWTでは記事を投稿できないこと",
        ),
        pytest.param(
            {
                "Authorization": f"Bearer {expired_jwt_token('caa93979-2256-42f0-8e83-55144674613b')}"
            },
            {"title": "タイトル", "text": "テキスト"},
            401,
            {"detail": "Token has expired."},
            id="有効期限切れのJWTでは記事を投稿できないこと",
        ),
    ],
)
def test_レスポンス(
    headers: dict | None, request_body: dict, status_code: int, json_response: dict
):
    with freeze_time(datetime(2025, 7, 23, 0, 0, 0)):
        response = client.post("/api/articles", headers=headers, json=request_body)

    assert response.status_code == status_code
    assert response.json() == json_response
