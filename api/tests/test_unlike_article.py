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
            id=uuid.UUID("7d4c6529-dd20-4856-a4c5-a33229e9ddfc"),
            user_id=uuid.UUID("caa93979-2256-42f0-8e83-55144674613b"),
            article_id=uuid.UUID("63a38d12-034e-4314-87d6-615b5ac0db44"),
        )
    ]

    session = next(get_mock_session())
    session.add_all(users + articles + like_articles)
    session.commit()


@pytest.mark.parametrize(
    "headers, id, status_code",
    [
        pytest.param(
            {
                "Authorization": f"Bearer {valid_jwt_token('caa93979-2256-42f0-8e83-55144674613b')}"
            },
            "7d4c6529-dd20-4856-a4c5-a33229e9ddfc",
            200,
            id="記事のいいねを解除できる場合",
        ),
        pytest.param(
            None,
            "7d4c6529-dd20-4856-a4c5-a33229e9ddfc",
            401,
            id="Bearerトークンがない場合",
        ),
        pytest.param(
            {
                "Authorization": f"Bearer {valid_jwt_token('407a9844-da17-4b58-b60c-500d35d2e45a')}"
            },
            "7d4c6529-dd20-4856-a4c5-a33229e9ddfc",
            401,
            id="存在しないユーザの場合",
        ),
        pytest.param(
            {
                "Authorization": f"Bearer {expired_jwt_token('caa93979-2256-42f0-8e83-55144674613b')}"
            },
            "7d4c6529-dd20-4856-a4c5-a33229e9ddfc",
            401,
            id="トークンの有効期限がない場合",
        ),
        pytest.param(
            {
                "Authorization": f"Bearer {valid_jwt_token('caa93979-2256-42f0-8e83-55144674613b')}"
            },
            "e1174d97-5432-4d4f-8fb3-1caf1359a02c",
            404,
            id="存在しない記事のいいねを解除した場合",
        ),
    ],
)
def test_ステータスコード(headers: dict | None, id: str, status_code: int):
    with freeze_time(datetime(2025, 7, 23, 0, 0, 0)):
        response = client.delete(f"/api/likes/{id}", headers=headers)

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "headers, id, result",
    [
        pytest.param(
            {
                "Authorization": f"Bearer {valid_jwt_token('caa93979-2256-42f0-8e83-55144674613b')}"
            },
            "7d4c6529-dd20-4856-a4c5-a33229e9ddfc",
            None,
            id="記事のいいねを解除できる場合",
        ),
        pytest.param(
            None,
            "7d4c6529-dd20-4856-a4c5-a33229e9ddfc",
            db_models.Like(
                id=uuid.UUID("7d4c6529-dd20-4856-a4c5-a33229e9ddfc"),
                user_id=uuid.UUID("caa93979-2256-42f0-8e83-55144674613b"),
                article_id=uuid.UUID("63a38d12-034e-4314-87d6-615b5ac0db44"),
            ),
            id="Bearerトークンがない場合",
        ),
        pytest.param(
            {
                "Authorization": f"Bearer {valid_jwt_token('407a9844-da17-4b58-b60c-500d35d2e45a')}"
            },
            "7d4c6529-dd20-4856-a4c5-a33229e9ddfc",
            db_models.Like(
                id=uuid.UUID("7d4c6529-dd20-4856-a4c5-a33229e9ddfc"),
                user_id=uuid.UUID("caa93979-2256-42f0-8e83-55144674613b"),
                article_id=uuid.UUID("63a38d12-034e-4314-87d6-615b5ac0db44"),
            ),
            id="存在しないユーザの場合",
        ),
        pytest.param(
            {
                "Authorization": f"Bearer {expired_jwt_token('caa93979-2256-42f0-8e83-55144674613b')}"
            },
            "7d4c6529-dd20-4856-a4c5-a33229e9ddfc",
            db_models.Like(
                id=uuid.UUID("7d4c6529-dd20-4856-a4c5-a33229e9ddfc"),
                user_id=uuid.UUID("caa93979-2256-42f0-8e83-55144674613b"),
                article_id=uuid.UUID("63a38d12-034e-4314-87d6-615b5ac0db44"),
            ),
            id="トークンの有効期限がない場合",
        ),
        pytest.param(
            {
                "Authorization": f"Bearer {valid_jwt_token('caa93979-2256-42f0-8e83-55144674613b')}"
            },
            "e1174d97-5432-4d4f-8fb3-1caf1359a02c",
            db_models.Like(
                id=uuid.UUID("7d4c6529-dd20-4856-a4c5-a33229e9ddfc"),
                user_id=uuid.UUID("caa93979-2256-42f0-8e83-55144674613b"),
                article_id=uuid.UUID("63a38d12-034e-4314-87d6-615b5ac0db44"),
            ),
            id="存在しない記事のいいねを解除した場合",
        ),
    ],
)
def test_DB登録内容(
    headers: dict | None,
    id: str,
    result: db_models.Like | None,
):
    with freeze_time(datetime(2025, 7, 23, 0, 0, 0)):
        client.delete(f"/api/likes/{id}", headers=headers)

    session = next(get_mock_session())
    like = session.get(
        db_models.Like, uuid.UUID("7d4c6529-dd20-4856-a4c5-a33229e9ddfc")
    )

    assert like == result
