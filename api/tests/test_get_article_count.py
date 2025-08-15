import pytest
from fastapi.testclient import TestClient

from app.infrastructure.db import db_models
from app.infrastructure.db.sqlite import get_mock_session
from app.main import app

client = TestClient(app)


@pytest.mark.parametrize("result", [pytest.param({"count": 3}, id="記事の件数を返す")])
def test_JSONレスポンス(result: dict[str, int]):
    session = next(get_mock_session())
    session.add_all(
        [
            db_models.Article(
                id="a6680a88-f226-4782-923d-4ed4a0f3697d",
                title="記事1",
                text="# Hello World",
                user_id="6e2aa5a1-f792-47b8-9393-58fd657e7451",
            ),
            db_models.Article(
                id="b6680a88-f226-4782-923d-4ed4a0f3697e",
                title="記事2",
                text="# FastAPI Testing",
                user_id="6e2aa5a1-f792-47b8-9393-58fd657e7451",
            ),
            db_models.Article(
                id="c6680a88-f226-4782-923d-4ed4a0f3697f",
                title="記事3",
                text="# Mocking in Tests",
                user_id="6e2aa5a1-f792-47b8-9393-58fd657e7451",
            ),
        ]
    )
    session.commit()

    response = client.get("/api/articles/count")

    assert response.json() == result
