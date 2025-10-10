import uuid
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from freezegun import freeze_time

from app.domain.entity.article import Article
from app.infrastructure.db import db_models
from app.infrastructure.db.sqlite import get_mock_session
from app.main import app
from tests.conftest import (
    MockDateTimeDefaultFactory,
    MockUUID,
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
    "headers, request_body, status_code",
    [
        pytest.param(
            {
                "Authorization": f"Bearer {valid_jwt_token('caa93979-2256-42f0-8e83-55144674613b')}"
            },
            {"title": "タイトル", "text": "テキスト"},
            201,
            id="記事を投稿できた場合",
        ),
        pytest.param(
            None,
            {"title": "タイトル", "text": "テキスト"},
            401,
            id="Bearerトークンがない場合",
        ),
        pytest.param(
            {
                "Authorization": f"Bearer {valid_jwt_token('407a9844-da17-4b58-b60c-500d35d2e45a')}"
            },
            {"title": "タイトル", "text": "テキスト"},
            401,
            id="存在しないユーザの場合",
        ),
        pytest.param(
            {
                "Authorization": f"Bearer {expired_jwt_token('caa93979-2256-42f0-8e83-55144674613b')}"
            },
            {"title": "タイトル", "text": "テキスト"},
            401,
            id="トークンの有効期限がない場合",
        ),
    ],
)
def test_ステータスコード(headers: dict | None, request_body: dict, status_code: int):
    with freeze_time(datetime(2025, 7, 23, 0, 0, 0)):
        response = client.post("/api/articles", headers=headers, json=request_body)

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "headers, request_body, result",
    [
        pytest.param(
            {
                "Authorization": f"Bearer {valid_jwt_token('caa93979-2256-42f0-8e83-55144674613b')}"
            },
            {"title": "タイトル", "text": "テキスト"},
            db_models.Article(
                id=uuid.UUID("f47ac10b-58cc-4372-a567-0e02b2c3d479"),
                title="タイトル",
                text="テキスト",
                published_at=datetime(2025, 7, 23, 0, 0, 0),
                user_id=uuid.UUID("caa93979-2256-42f0-8e83-55144674613b"),
            ),
            id="記事を投稿できた場合",
        ),
        pytest.param(
            None,
            {"title": "タイトル", "text": "テキスト"},
            None,
            id="Bearerトークンがない場合",
        ),
        pytest.param(
            {
                "Authorization": f"Bearer {valid_jwt_token('407a9844-da17-4b58-b60c-500d35d2e45a')}"
            },
            {"title": "タイトル", "text": "テキスト"},
            None,
            id="存在しないユーザの場合",
        ),
        pytest.param(
            {
                "Authorization": f"Bearer {expired_jwt_token('caa93979-2256-42f0-8e83-55144674613b')}"
            },
            {"title": "タイトル", "text": "テキスト"},
            None,
            id="トークンの有効期限がない場合",
        ),
    ],
)
def test_DB登録内容(
    headers: dict,
    request_body: dict,
    result: db_models.Article | None,
    mock_uuid: MockUUID,
    mock_datetime_default_factory: MockDateTimeDefaultFactory,
):
    mock_uuid(
        Article,
        Article.model_fields["id"],
        uuid.UUID("f47ac10b-58cc-4372-a567-0e02b2c3d479"),
    )
    mock_datetime_default_factory(
        Article,
        Article.model_fields["published_at"],
        datetime(2025, 7, 23, 0, 0, 0),
    )

    with freeze_time(datetime(2025, 7, 23, 0, 0, 0)):
        client.post("/api/articles", headers=headers, json=request_body)

    session = next(get_mock_session())
    article = session.get(
        db_models.Article, uuid.UUID("f47ac10b-58cc-4372-a567-0e02b2c3d479")
    )

    assert article == result
