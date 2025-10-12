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
    "id, status_code, json_response",
    [
        pytest.param(
            "63a38d12-034e-4314-87d6-615b5ac0db44",
            200,
            {
                "id": "63a38d12-034e-4314-87d6-615b5ac0db44",
                "title": "記事1",
                "text": "# Hello World",
                "published_at": "2025-07-23T00:00:00",
                "user": {
                    "id": "caa93979-2256-42f0-8e83-55144674613b",
                    "name": "sh-okada",
                },
            },
            id="idと一致する記事が取得できること",
        ),
        pytest.param(
            "e88e396b-d6fa-4660-a5a6-a5af0f2638be",
            404,
            {"detail": "Article not found."},
            id="idと一致する記事がない場合は404エラーになること",
        ),
    ],
)
def test_レスポンス(id: uuid.UUID, status_code: int, json_response: dict):
    user = db_models.User(
        id=uuid.UUID("caa93979-2256-42f0-8e83-55144674613b"),
        name="sh-okada",
        password="$2b$12$ypi5a45bRgKPo4ZJk2IvQeqKJLlfpmGGwL9Pu9i/rEs2Pa0y7SywS",
    )
    article = db_models.Article(
        id=uuid.UUID("63a38d12-034e-4314-87d6-615b5ac0db44"),
        title="記事1",
        text="# Hello World",
        published_at=datetime(2025, 7, 23, 0, 0, 0),
        user_id=uuid.UUID("caa93979-2256-42f0-8e83-55144674613b"),
    )

    session = next(get_mock_session())
    session.add_all([user, article])
    session.commit()

    with freeze_time(datetime(2025, 7, 23, 0, 0, 0)):
        response = client.get(f"/api/articles/{id}")

    assert response.status_code == status_code
    assert response.json() == json_response
