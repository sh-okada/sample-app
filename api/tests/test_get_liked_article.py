import uuid
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from freezegun import freeze_time

from app.infrastructure.db import db_models
from app.infrastructure.db.sqlite import get_mock_session
from app.main import app
from tests.conftest import expired_access_token, valid_access_token

client = TestClient(app)


@pytest.mark.parametrize(
    "headers, id, status_code, json_response",
    [
        pytest.param(
            {
                "Authorization": f"Bearer {valid_access_token('caa93979-2256-42f0-8e83-55144674613b')}"
            },
            "f3869b72-1f0a-433a-96b0-d9b934234936",
            200,
            {
                "id": "f3869b72-1f0a-433a-96b0-d9b934234936",
                "title": "記事2",
                "text": "# Hello World",
                "published_at": "2025-07-23T00:00:00",
                "user": {
                    "id": "2a7680c3-ad35-4734-93ac-b7c088c86a53",
                    "name": "ec-okada",
                },
            },
            id="idと一致するいいねした記事が取得できること",
        ),
        pytest.param(
            None,
            "f3869b72-1f0a-433a-96b0-d9b934234936",
            401,
            {"detail": "Not authenticated"},
            id="JWTがない状態でいいねした記事を取得できないこと",
        ),
        pytest.param(
            {"Authorization": "Bearer invalid-token"},
            "f3869b72-1f0a-433a-96b0-d9b934234936",
            401,
            {"detail": "Invalid token."},
            id="不正なJWTではいいねした記事が取得できないこと",
        ),
        pytest.param(
            {
                "Authorization": f"Bearer {valid_access_token('407a9844-da17-4b58-b60c-500d35d2e45a')}"
            },
            "f3869b72-1f0a-433a-96b0-d9b934234936",
            401,
            {"detail": "User not found."},
            id="存在しないユーザーのJWTではいいねした記事が取得できないこと",
        ),
        pytest.param(
            {
                "Authorization": f"Bearer {expired_access_token('caa93979-2256-42f0-8e83-55144674613b')}"
            },
            "f3869b72-1f0a-433a-96b0-d9b934234936",
            401,
            {"detail": "Token has expired."},
            id="有効期限切れのJWTではいいねした記事が取得できないこと",
        ),
        pytest.param(
            {
                "Authorization": f"Bearer {valid_access_token('caa93979-2256-42f0-8e83-55144674613b')}"
            },
            "e88e396b-d6fa-4660-a5a6-a5af0f2638be",
            404,
            {"detail": "Liked article not found."},
            id="idと一致する記事がない場合は404エラーになること",
        ),
    ],
)
def test_レスポンス(
    headers: dict | None, id: uuid.UUID, status_code: int, json_response: dict
):
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
            published_at=datetime(2025, 7, 23, 0, 0, 0),
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

    with freeze_time(datetime(2025, 7, 23, 0, 0, 0)):
        response = client.get(f"/api/users/me/liked-articles/{id}", headers=headers)

    assert response.status_code == status_code
    assert response.json() == json_response
