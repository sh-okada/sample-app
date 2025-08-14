import pytest
from fastapi.testclient import TestClient

from app.infrastructure.db import db_models
from app.infrastructure.db.sqlite import get_mock_session
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def before_each():
    user = db_models.User(
        id="caa93979-2256-42f0-8e83-55144674613b",
        name="sh-okada",
        password="$2b$12$ypi5a45bRgKPo4ZJk2IvQeqKJLlfpmGGwL9Pu9i/rEs2Pa0y7SywS",
    )
    article = db_models.Article(
        id="63a38d12-034e-4314-87d6-615b5ac0db44",
        title="記事1",
        text="# Hello World",
        user_id="caa93979-2256-42f0-8e83-55144674613b",
    )

    session = next(get_mock_session())
    session.add_all([user, article])
    session.commit()


@pytest.mark.parametrize(
    "article_id, status_code",
    [
        pytest.param(
            "63a38d12-034e-4314-87d6-615b5ac0db44",
            200,
            id="記事が存在する場合",
        ),
        pytest.param(
            "e88e396b-d6fa-4660-a5a6-a5af0f2638be",
            404,
            id="記事が存在しない場合",
        ),
        pytest.param(
            "1",
            422,
            id="article_idが1文字以下",
        ),
        pytest.param(
            "12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901",
            422,
            id="article_idが101文字以上",
        ),
    ],
)
def test_ステータスコード(article_id: str, status_code: int):
    response = client.get(f"/api/articles/{article_id}")

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "article_id, json_response",
    [
        pytest.param(
            "63a38d12-034e-4314-87d6-615b5ac0db44",
            {
                "id": "63a38d12-034e-4314-87d6-615b5ac0db44",
                "title": "記事1",
                "text": "# Hello World",
                "user": {
                    "id": "caa93979-2256-42f0-8e83-55144674613b",
                    "name": "sh-okada",
                },
            },
            id="記事が存在する場合のレスポンス",
        ),
        pytest.param(
            "e88e396b-d6fa-4660-a5a6-a5af0f2638be",
            {"detail": "Not Found"},
            id="記事が存在しない場合のレスポンス",
        ),
    ],
)
def test_json_response(article_id: str, json_response: dict):
    response = client.get(f"/api/articles/{article_id}")

    assert response.json() == json_response
