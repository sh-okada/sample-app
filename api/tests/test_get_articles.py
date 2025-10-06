import uuid

import pytest
from fastapi.testclient import TestClient

from app.infrastructure.db import db_models
from app.infrastructure.db.sqlite import get_mock_session
from app.main import app

client = TestClient(app)


@pytest.mark.parametrize(
    "query_params, status_code",
    [
        pytest.param(
            {"page": 1, "limit": 5},
            200,
            id="page=1&limit=5",
        ),
        pytest.param({"q": "React"}, 200, id="q=Reactの場合"),
        pytest.param(
            {"limit": 4},
            422,
            id="limitが4以下の場合",
        ),
        pytest.param(
            {"limit": 101},
            422,
            id="limitが101以上の場合",
        ),
        pytest.param(
            {"page": 0},
            422,
            id="pageが0以下の場合",
        ),
        pytest.param(
            {"page": 10001},
            422,
            id="pageが10001以上の場合",
        ),
        pytest.param(
            {"q": "a" * 101},
            422,
            id="qが100文字以上の場合",
        ),
    ],
)
def test_ステータスコード(query_params: dict, status_code: int):
    response = client.get("/api/articles", params=query_params)

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "query_params, json_response",
    [
        pytest.param(
            {},
            [
                {
                    "id": "a6680a88-f226-4782-923d-4ed4a0f3697d",
                    "title": "記事1",
                    "text": "# Hello World",
                    "user": {
                        "id": "6e2aa5a1-f792-47b8-9393-58fd657e7451",
                        "name": "sh-okada",
                    },
                },
                {
                    "id": "f3869b72-1f0a-433a-96b0-d9b934234936",
                    "title": "記事2",
                    "text": "# Hello World",
                    "user": {
                        "id": "2a7680c3-ad35-4734-93ac-b7c088c86a53",
                        "name": "ec-okada",
                    },
                },
                {
                    "id": "383853ee-a7b9-4792-aad8-aad82e5cc072",
                    "title": "記事3",
                    "text": "# Hello World",
                    "user": {
                        "id": "2a7680c3-ad35-4734-93ac-b7c088c86a53",
                        "name": "ec-okada",
                    },
                },
                {
                    "id": "fbb7be33-bb8f-4ace-97af-8d711040dd99",
                    "title": "記事4",
                    "text": "# Hello World",
                    "user": {
                        "id": "2a7680c3-ad35-4734-93ac-b7c088c86a53",
                        "name": "ec-okada",
                    },
                },
                {
                    "id": "6f027d9d-040c-4c51-a135-edff8b44c331",
                    "title": "記事5",
                    "text": "# Hello World",
                    "user": {
                        "id": "2a7680c3-ad35-4734-93ac-b7c088c86a53",
                        "name": "ec-okada",
                    },
                },
            ],
            id="page=1&limit=5",
        ),
        pytest.param(
            {"limit": 10},
            [
                {
                    "id": "a6680a88-f226-4782-923d-4ed4a0f3697d",
                    "title": "記事1",
                    "text": "# Hello World",
                    "user": {
                        "id": "6e2aa5a1-f792-47b8-9393-58fd657e7451",
                        "name": "sh-okada",
                    },
                },
                {
                    "id": "f3869b72-1f0a-433a-96b0-d9b934234936",
                    "title": "記事2",
                    "text": "# Hello World",
                    "user": {
                        "id": "2a7680c3-ad35-4734-93ac-b7c088c86a53",
                        "name": "ec-okada",
                    },
                },
                {
                    "id": "383853ee-a7b9-4792-aad8-aad82e5cc072",
                    "title": "記事3",
                    "text": "# Hello World",
                    "user": {
                        "id": "2a7680c3-ad35-4734-93ac-b7c088c86a53",
                        "name": "ec-okada",
                    },
                },
                {
                    "id": "fbb7be33-bb8f-4ace-97af-8d711040dd99",
                    "title": "記事4",
                    "text": "# Hello World",
                    "user": {
                        "id": "2a7680c3-ad35-4734-93ac-b7c088c86a53",
                        "name": "ec-okada",
                    },
                },
                {
                    "id": "6f027d9d-040c-4c51-a135-edff8b44c331",
                    "title": "記事5",
                    "text": "# Hello World",
                    "user": {
                        "id": "2a7680c3-ad35-4734-93ac-b7c088c86a53",
                        "name": "ec-okada",
                    },
                },
                {
                    "id": "4e093992-8f3d-424d-8fda-733884197230",
                    "title": "記事6",
                    "text": "# Hello World",
                    "user": {
                        "id": "2a7680c3-ad35-4734-93ac-b7c088c86a53",
                        "name": "ec-okada",
                    },
                },
            ],
            id="limit=10の場合",
        ),
        pytest.param(
            {"page": 2},
            [
                {
                    "id": "4e093992-8f3d-424d-8fda-733884197230",
                    "title": "記事6",
                    "text": "# Hello World",
                    "user": {
                        "id": "2a7680c3-ad35-4734-93ac-b7c088c86a53",
                        "name": "ec-okada",
                    },
                },
            ],
            id="page=2の場合",
        ),
        pytest.param(
            {"page": 3},
            [],
            id="page=3の場合",
        ),
        pytest.param(
            {"q": "記事1"},
            [
                {
                    "id": "a6680a88-f226-4782-923d-4ed4a0f3697d",
                    "title": "記事1",
                    "text": "# Hello World",
                    "user": {
                        "id": "6e2aa5a1-f792-47b8-9393-58fd657e7451",
                        "name": "sh-okada",
                    },
                }
            ],
            id="q=記事1の場合",
        ),
    ],
)
def test_JSONレスポンス(query_params: dict, json_response: list[dict]):
    users = [
        db_models.User(
            id=uuid.UUID("6e2aa5a1-f792-47b8-9393-58fd657e7451"),
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
            id=uuid.UUID("a6680a88-f226-4782-923d-4ed4a0f3697d"),
            title="記事1",
            text="# Hello World",
            user_id=uuid.UUID("6e2aa5a1-f792-47b8-9393-58fd657e7451"),
        ),
        db_models.Article(
            id=uuid.UUID("f3869b72-1f0a-433a-96b0-d9b934234936"),
            title="記事2",
            text="# Hello World",
            user_id=uuid.UUID("2a7680c3-ad35-4734-93ac-b7c088c86a53"),
        ),
        db_models.Article(
            id=uuid.UUID("383853ee-a7b9-4792-aad8-aad82e5cc072"),
            title="記事3",
            text="# Hello World",
            user_id=uuid.UUID("2a7680c3-ad35-4734-93ac-b7c088c86a53"),
        ),
        db_models.Article(
            id=uuid.UUID("fbb7be33-bb8f-4ace-97af-8d711040dd99"),
            title="記事4",
            text="# Hello World",
            user_id=uuid.UUID("2a7680c3-ad35-4734-93ac-b7c088c86a53"),
        ),
        db_models.Article(
            id=uuid.UUID("6f027d9d-040c-4c51-a135-edff8b44c331"),
            title="記事5",
            text="# Hello World",
            user_id=uuid.UUID("2a7680c3-ad35-4734-93ac-b7c088c86a53"),
        ),
        db_models.Article(
            id=uuid.UUID("4e093992-8f3d-424d-8fda-733884197230"),
            title="記事6",
            text="# Hello World",
            user_id=uuid.UUID("2a7680c3-ad35-4734-93ac-b7c088c86a53"),
        ),
    ]

    session = next(get_mock_session())
    session.add_all(users + articles)
    session.commit()

    response = client.get("/api/articles", params=query_params)

    assert response.json() == json_response
