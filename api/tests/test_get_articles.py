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
    "query_params, status_code, json_response",
    [
        pytest.param(
            None,
            200,
            {
                "values": [],
                "count": 0,
                "total_pages": 0,
            },
            id="記事の一覧がJSONで取得できること",
        ),
        pytest.param(
            {"limit": 4},
            422,
            {
                "detail": [
                    {
                        "type": "greater_than_equal",
                        "loc": ["query", "limit"],
                        "msg": "Input should be greater than or equal to 5",
                        "input": "4",
                        "ctx": {"ge": 5},
                    }
                ]
            },
            id="クエリパラメータのlimitは5以上であること",
        ),
        pytest.param(
            {"limit": 101},
            422,
            {
                "detail": [
                    {
                        "type": "less_than_equal",
                        "loc": ["query", "limit"],
                        "msg": "Input should be less than or equal to 100",
                        "input": "101",
                        "ctx": {"le": 100},
                    }
                ]
            },
            id="クエリパラメータのlimitは100以下であること",
        ),
        pytest.param(
            {"page": 0},
            422,
            {
                "detail": [
                    {
                        "type": "greater_than_equal",
                        "loc": ["query", "page"],
                        "msg": "Input should be greater than or equal to 1",
                        "input": "0",
                        "ctx": {"ge": 1},
                    }
                ]
            },
            id="クエリパラメータのpageは1以上であること",
        ),
        pytest.param(
            {"page": 10001},
            422,
            {
                "detail": [
                    {
                        "type": "less_than_equal",
                        "loc": ["query", "page"],
                        "msg": "Input should be less than or equal to 10000",
                        "input": "10001",
                        "ctx": {"le": 10000},
                    }
                ]
            },
            id="クエリパラメータのpageは10000以下であること",
        ),
        pytest.param(
            {
                "q": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
            },
            422,
            {
                "detail": [
                    {
                        "type": "string_too_long",
                        "loc": ["query", "q"],
                        "msg": "String should have at most 100 characters",
                        "input": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                        "ctx": {"max_length": 100},
                    }
                ]
            },
            id="クエリパラメータのqは100文字以下であること",
        ),
    ],
)
def test_レスポンス(query_params: dict, status_code: int, json_response: dict):
    with freeze_time(datetime(2025, 7, 23, 0, 0, 0)):
        response = client.get("/api/articles", params=query_params)

    assert response.status_code == status_code
    assert response.json() == json_response


@pytest.mark.parametrize(
    "query_params, json_response",
    [
        pytest.param(
            {},
            {
                "values": [
                    {
                        "id": "4e093992-8f3d-424d-8fda-733884197230",
                        "title": "記事6",
                        "text": "# Hello World",
                        "published_at": "2025-07-23T06:00:00",
                        "user": {
                            "id": "2a7680c3-ad35-4734-93ac-b7c088c86a53",
                            "name": "ec-okada",
                        },
                    },
                    {
                        "id": "6f027d9d-040c-4c51-a135-edff8b44c331",
                        "title": "記事5",
                        "text": "# Hello World",
                        "published_at": "2025-07-23T05:00:00",
                        "user": {
                            "id": "2a7680c3-ad35-4734-93ac-b7c088c86a53",
                            "name": "ec-okada",
                        },
                    },
                    {
                        "id": "fbb7be33-bb8f-4ace-97af-8d711040dd99",
                        "title": "記事4",
                        "text": "# Hello World",
                        "published_at": "2025-07-23T04:00:00",
                        "user": {
                            "id": "2a7680c3-ad35-4734-93ac-b7c088c86a53",
                            "name": "ec-okada",
                        },
                    },
                    {
                        "id": "383853ee-a7b9-4792-aad8-aad82e5cc072",
                        "title": "記事3",
                        "text": "# Hello World",
                        "published_at": "2025-07-23T03:00:00",
                        "user": {
                            "id": "2a7680c3-ad35-4734-93ac-b7c088c86a53",
                            "name": "ec-okada",
                        },
                    },
                    {
                        "id": "f3869b72-1f0a-433a-96b0-d9b934234936",
                        "title": "記事2",
                        "text": "# Hello World",
                        "published_at": "2025-07-23T02:00:00",
                        "user": {
                            "id": "2a7680c3-ad35-4734-93ac-b7c088c86a53",
                            "name": "ec-okada",
                        },
                    },
                ],
                "count": 6,
                "total_pages": 2,
            },
            id="q=&page=1&limit=5がデフォルトになること",
        ),
        pytest.param(
            {"limit": 10},
            {
                "values": [
                    {
                        "id": "4e093992-8f3d-424d-8fda-733884197230",
                        "title": "記事6",
                        "text": "# Hello World",
                        "published_at": "2025-07-23T06:00:00",
                        "user": {
                            "id": "2a7680c3-ad35-4734-93ac-b7c088c86a53",
                            "name": "ec-okada",
                        },
                    },
                    {
                        "id": "6f027d9d-040c-4c51-a135-edff8b44c331",
                        "title": "記事5",
                        "text": "# Hello World",
                        "published_at": "2025-07-23T05:00:00",
                        "user": {
                            "id": "2a7680c3-ad35-4734-93ac-b7c088c86a53",
                            "name": "ec-okada",
                        },
                    },
                    {
                        "id": "fbb7be33-bb8f-4ace-97af-8d711040dd99",
                        "title": "記事4",
                        "text": "# Hello World",
                        "published_at": "2025-07-23T04:00:00",
                        "user": {
                            "id": "2a7680c3-ad35-4734-93ac-b7c088c86a53",
                            "name": "ec-okada",
                        },
                    },
                    {
                        "id": "383853ee-a7b9-4792-aad8-aad82e5cc072",
                        "title": "記事3",
                        "text": "# Hello World",
                        "published_at": "2025-07-23T03:00:00",
                        "user": {
                            "id": "2a7680c3-ad35-4734-93ac-b7c088c86a53",
                            "name": "ec-okada",
                        },
                    },
                    {
                        "id": "f3869b72-1f0a-433a-96b0-d9b934234936",
                        "title": "記事2",
                        "text": "# Hello World",
                        "published_at": "2025-07-23T02:00:00",
                        "user": {
                            "id": "2a7680c3-ad35-4734-93ac-b7c088c86a53",
                            "name": "ec-okada",
                        },
                    },
                    {
                        "id": "a6680a88-f226-4782-923d-4ed4a0f3697d",
                        "title": "記事1",
                        "text": "# Hello World",
                        "published_at": "2025-07-23T01:00:00",
                        "user": {
                            "id": "6e2aa5a1-f792-47b8-9393-58fd657e7451",
                            "name": "sh-okada",
                        },
                    },
                ],
                "count": 6,
                "total_pages": 1,
            },
            id="一度に取得できる記事の件数がlimitで指定できること",
        ),
        pytest.param(
            {"page": 2},
            {
                "values": [
                    {
                        "id": "a6680a88-f226-4782-923d-4ed4a0f3697d",
                        "title": "記事1",
                        "text": "# Hello World",
                        "published_at": "2025-07-23T01:00:00",
                        "user": {
                            "id": "6e2aa5a1-f792-47b8-9393-58fd657e7451",
                            "name": "sh-okada",
                        },
                    },
                ],
                "count": 6,
                "total_pages": 2,
            },
            id="pageで指定したページの記事一覧が取得できること",
        ),
        pytest.param(
            {"page": 3},
            {
                "values": [],
                "count": 6,
                "total_pages": 2,
            },
            id="total_pagesを超えると空の記事一覧が取得できること",
        ),
        pytest.param(
            {"q": "記事1"},
            {
                "values": [
                    {
                        "id": "a6680a88-f226-4782-923d-4ed4a0f3697d",
                        "title": "記事1",
                        "text": "# Hello World",
                        "published_at": "2025-07-23T01:00:00",
                        "user": {
                            "id": "6e2aa5a1-f792-47b8-9393-58fd657e7451",
                            "name": "sh-okada",
                        },
                    }
                ],
                "count": 1,
                "total_pages": 1,
            },
            id="qで指定した文字列がタイトルに含まれる記事一覧が取得できること",
        ),
        pytest.param(
            {"q": "存在しない記事"},
            {
                "values": [],
                "count": 0,
                "total_pages": 0,
            },
            id="qで指定した文字列がタイトルに含まれる記事がない場合、空の記事一覧が取得できること",
        ),
    ],
)
def test_クエリパラメータ(query_params: dict, json_response: list[dict]):
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
            published_at=datetime(2025, 7, 23, 1, 0, 0),
            user_id=uuid.UUID("6e2aa5a1-f792-47b8-9393-58fd657e7451"),
        ),
        db_models.Article(
            id=uuid.UUID("f3869b72-1f0a-433a-96b0-d9b934234936"),
            title="記事2",
            text="# Hello World",
            published_at=datetime(2025, 7, 23, 2, 0, 0),
            user_id=uuid.UUID("2a7680c3-ad35-4734-93ac-b7c088c86a53"),
        ),
        db_models.Article(
            id=uuid.UUID("383853ee-a7b9-4792-aad8-aad82e5cc072"),
            title="記事3",
            text="# Hello World",
            published_at=datetime(2025, 7, 23, 3, 0, 0),
            user_id=uuid.UUID("2a7680c3-ad35-4734-93ac-b7c088c86a53"),
        ),
        db_models.Article(
            id=uuid.UUID("fbb7be33-bb8f-4ace-97af-8d711040dd99"),
            title="記事4",
            text="# Hello World",
            published_at=datetime(2025, 7, 23, 4, 0, 0),
            user_id=uuid.UUID("2a7680c3-ad35-4734-93ac-b7c088c86a53"),
        ),
        db_models.Article(
            id=uuid.UUID("6f027d9d-040c-4c51-a135-edff8b44c331"),
            title="記事5",
            text="# Hello World",
            published_at=datetime(2025, 7, 23, 5, 0, 0),
            user_id=uuid.UUID("2a7680c3-ad35-4734-93ac-b7c088c86a53"),
        ),
        db_models.Article(
            id=uuid.UUID("4e093992-8f3d-424d-8fda-733884197230"),
            title="記事6",
            text="# Hello World",
            published_at=datetime(2025, 7, 23, 6, 0, 0),
            user_id=uuid.UUID("2a7680c3-ad35-4734-93ac-b7c088c86a53"),
        ),
    ]

    session = next(get_mock_session())
    session.add_all(users + articles)
    session.commit()

    with freeze_time(datetime(2025, 7, 23, 0, 0, 0)):
        response = client.get("/api/articles", params=query_params)

    assert response.json() == json_response
