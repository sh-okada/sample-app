import uuid
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from freezegun import freeze_time

from app.infrastructure.db import db_models
from app.infrastructure.db.sqlite import get_mock_session
from app.main import app
from tests.conftest import expired_jwt_token, valid_jwt_token

client = TestClient(app)


@pytest.fixture(autouse=True)
def before_each():
    users = [
        db_models.User(
            id=uuid.UUID("caa93979-2256-42f0-8e83-55144674613b"),
            name="sh-okada",
            password="$2b$12$ypi5a45bRgKPo4ZJk2IvQeqKJLlfpmGGwL9Pu9i/rEs2Pa0y7SywS",
        ),
        db_models.User(
            id=uuid.UUID("2a7680c3-ad35-4734-93ac-b7c088c86a53"),
            name="ec-okada",
            password="$2b$12$ypi5a45bRgKPo4ZJk2IvQeqKJLlfpmGGwL9Pu9i/rEs2Pa0y7SywS",
        ),
    ]

    articles = [
        db_models.Article(
            id=uuid.UUID("63a38d12-034e-4314-87d6-615b5ac0db44"),
            title="記事1",
            text="# Hello World",
            published_at=datetime(2025, 7, 23, 0, 0, 0),
            user_id=uuid.UUID("caa93979-2256-42f0-8e83-55144674613b"),
        ),
        db_models.Article(
            id=uuid.UUID("f3869b72-1f0a-433a-96b0-d9b934234936"),
            title="記事2",
            text="# Hello World",
            published_at=datetime(2025, 7, 23, 2, 0, 0),
            user_id=uuid.UUID("2a7680c3-ad35-4734-93ac-b7c088c86a53"),
        ),
    ]

    like_articles = [
        db_models.Like(
            user_id=uuid.UUID("caa93979-2256-42f0-8e83-55144674613b"),
            article_id=uuid.UUID("f3869b72-1f0a-433a-96b0-d9b934234936"),
        )
    ]

    session = next(get_mock_session())
    session.add_all(users + articles + like_articles)
    session.commit()


@pytest.mark.parametrize(
    "headers, request_body, status_code",
    [
        pytest.param(
            {
                "Authorization": f"Bearer {valid_jwt_token('2a7680c3-ad35-4734-93ac-b7c088c86a53')}"
            },
            {"article_id": "63a38d12-034e-4314-87d6-615b5ac0db44"},
            201,
            id="記事にいいねできた場合",
        ),
        pytest.param(
            {
                "Authorization": f"Bearer {valid_jwt_token('caa93979-2256-42f0-8e83-55144674613b')}"
            },
            {"article_id": "63a38d12-034e-4314-87d6-615b5ac0db44"},
            400,
            id="自分の記事にいいねした場合",
        ),
        pytest.param(
            {
                "Authorization": f"Bearer {valid_jwt_token('caa93979-2256-42f0-8e83-55144674613b')}"
            },
            {"article_id": "f3869b72-1f0a-433a-96b0-d9b934234936"},
            400,
            id="既に記事にいいねをしている場合",
        ),
        pytest.param(
            None,
            {"article_id": "63a38d12-034e-4314-87d6-615b5ac0db44"},
            401,
            id="Bearerトークンがない場合",
        ),
        pytest.param(
            {
                "Authorization": f"Bearer {valid_jwt_token('407a9844-da17-4b58-b60c-500d35d2e45a')}"
            },
            {"article_id": "63a38d12-034e-4314-87d6-615b5ac0db44"},
            401,
            id="存在しないユーザの場合",
        ),
        pytest.param(
            {
                "Authorization": f"Bearer {expired_jwt_token('caa93979-2256-42f0-8e83-55144674613b')}"
            },
            {"article_id": "63a38d12-034e-4314-87d6-615b5ac0db44"},
            401,
            id="トークンの有効期限がない場合",
        ),
        pytest.param(
            {
                "Authorization": f"Bearer {valid_jwt_token('2a7680c3-ad35-4734-93ac-b7c088c86a53')}"
            },
            {"article_id": "338e404d-6125-46e5-8bd1-054241a4ea43"},
            404,
            id="存在しない記事にいいねした場合",
        ),
    ],
)
def test_ステータスコード(headers: dict | None, request_body: dict, status_code: int):
    with freeze_time(datetime(2025, 7, 23, 0, 0, 0)):
        response = client.post(
            "/api/users/me/liked-articles", headers=headers, json=request_body
        )

    assert response.status_code == status_code
