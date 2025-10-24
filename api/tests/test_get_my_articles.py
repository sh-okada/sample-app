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
    "headers, status_code, json_response",
    [
        pytest.param(
            {
                "Authorization": f"Bearer {valid_access_token('caa93979-2256-42f0-8e83-55144674613b')}"
            },
            200,
            {
                "values": [
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
                    {
                        "id": "d019292a-538b-431c-ad9a-453013812c65",
                        "title": "記事3",
                        "text": "# Hello World",
                        "published_at": "2025-07-23T00:00:00",
                        "user": {
                            "id": "caa93979-2256-42f0-8e83-55144674613b",
                            "name": "sh-okada",
                        },
                    },
                ],
                "count": 2,
                "total_pages": 1,
            },
            id="自分が投稿した記事が取得できること",
        ),
        pytest.param(
            None,
            401,
            {"detail": "Not authenticated"},
            id="JWTがない状態で自分が投稿した記事が取得を取得できないこと",
        ),
        pytest.param(
            {"Authorization": "Bearer invalid-token"},
            401,
            {"detail": "Invalid token."},
            id="不正なJWTでは自分が投稿した記事が取得が取得できないこと",
        ),
        pytest.param(
            {
                "Authorization": f"Bearer {valid_access_token('407a9844-da17-4b58-b60c-500d35d2e45a')}"
            },
            401,
            {"detail": "User not found."},
            id="存在しないユーザーのJWTでは自分が投稿した記事が取得が取得できないこと",
        ),
        pytest.param(
            {
                "Authorization": f"Bearer {expired_access_token('caa93979-2256-42f0-8e83-55144674613b')}"
            },
            401,
            {"detail": "Token has expired."},
            id="有効期限切れのJWTでは自分が投稿した記事が取得が取得できないこと",
        ),
    ],
)
def test_レスポンス(headers: dict | None, status_code: int, json_response: dict):
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
        db_models.Article(
            id=uuid.UUID("d019292a-538b-431c-ad9a-453013812c65"),
            title="記事3",
            text="# Hello World",
            published_at=datetime(2025, 7, 23, 0, 0, 0),
            user_id=uuid.UUID("caa93979-2256-42f0-8e83-55144674613b"),
        ),
    ]

    session = next(get_mock_session())
    session.add_all(users + articles)
    session.commit()

    with freeze_time(datetime(2025, 7, 23, 0, 0, 0)):
        response = client.get("/api/users/me/articles", headers=headers)

    assert response.status_code == status_code
    assert response.json() == json_response


@pytest.mark.parametrize(
    "headers, query_params, json_response",
    [
        pytest.param(
            {
                "Authorization": f"Bearer {valid_access_token('6e2aa5a1-f792-47b8-9393-58fd657e7451')}"
            },
            {},
            {
                "values": [
                    {
                        "id": "4e093992-8f3d-424d-8fda-733884197230",
                        "title": "記事6",
                        "text": "# Hello World",
                        "published_at": "2025-07-23T06:00:00",
                        "user": {
                            "id": "6e2aa5a1-f792-47b8-9393-58fd657e7451",
                            "name": "sh-okada",
                        },
                    },
                    {
                        "id": "6f027d9d-040c-4c51-a135-edff8b44c331",
                        "title": "記事5",
                        "text": "# Hello World",
                        "published_at": "2025-07-23T05:00:00",
                        "user": {
                            "id": "6e2aa5a1-f792-47b8-9393-58fd657e7451",
                            "name": "sh-okada",
                        },
                    },
                    {
                        "id": "fbb7be33-bb8f-4ace-97af-8d711040dd99",
                        "title": "記事4",
                        "text": "# Hello World",
                        "published_at": "2025-07-23T04:00:00",
                        "user": {
                            "id": "6e2aa5a1-f792-47b8-9393-58fd657e7451",
                            "name": "sh-okada",
                        },
                    },
                    {
                        "id": "383853ee-a7b9-4792-aad8-aad82e5cc072",
                        "title": "記事3",
                        "text": "# Hello World",
                        "published_at": "2025-07-23T03:00:00",
                        "user": {
                            "id": "6e2aa5a1-f792-47b8-9393-58fd657e7451",
                            "name": "sh-okada",
                        },
                    },
                    {
                        "id": "f3869b72-1f0a-433a-96b0-d9b934234936",
                        "title": "記事2",
                        "text": "# Hello World",
                        "published_at": "2025-07-23T02:00:00",
                        "user": {
                            "id": "6e2aa5a1-f792-47b8-9393-58fd657e7451",
                            "name": "sh-okada",
                        },
                    },
                ],
                "count": 6,
                "total_pages": 2,
            },
            id="q=&page=1&limit=5がデフォルトになること",
        ),
        pytest.param(
            {
                "Authorization": f"Bearer {valid_access_token('6e2aa5a1-f792-47b8-9393-58fd657e7451')}"
            },
            {"limit": 10},
            {
                "values": [
                    {
                        "id": "4e093992-8f3d-424d-8fda-733884197230",
                        "title": "記事6",
                        "text": "# Hello World",
                        "published_at": "2025-07-23T06:00:00",
                        "user": {
                            "id": "6e2aa5a1-f792-47b8-9393-58fd657e7451",
                            "name": "sh-okada",
                        },
                    },
                    {
                        "id": "6f027d9d-040c-4c51-a135-edff8b44c331",
                        "title": "記事5",
                        "text": "# Hello World",
                        "published_at": "2025-07-23T05:00:00",
                        "user": {
                            "id": "6e2aa5a1-f792-47b8-9393-58fd657e7451",
                            "name": "sh-okada",
                        },
                    },
                    {
                        "id": "fbb7be33-bb8f-4ace-97af-8d711040dd99",
                        "title": "記事4",
                        "text": "# Hello World",
                        "published_at": "2025-07-23T04:00:00",
                        "user": {
                            "id": "6e2aa5a1-f792-47b8-9393-58fd657e7451",
                            "name": "sh-okada",
                        },
                    },
                    {
                        "id": "383853ee-a7b9-4792-aad8-aad82e5cc072",
                        "title": "記事3",
                        "text": "# Hello World",
                        "published_at": "2025-07-23T03:00:00",
                        "user": {
                            "id": "6e2aa5a1-f792-47b8-9393-58fd657e7451",
                            "name": "sh-okada",
                        },
                    },
                    {
                        "id": "f3869b72-1f0a-433a-96b0-d9b934234936",
                        "title": "記事2",
                        "text": "# Hello World",
                        "published_at": "2025-07-23T02:00:00",
                        "user": {
                            "id": "6e2aa5a1-f792-47b8-9393-58fd657e7451",
                            "name": "sh-okada",
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
            {
                "Authorization": f"Bearer {valid_access_token('6e2aa5a1-f792-47b8-9393-58fd657e7451')}"
            },
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
            {
                "Authorization": f"Bearer {valid_access_token('6e2aa5a1-f792-47b8-9393-58fd657e7451')}"
            },
            {"page": 3},
            {
                "values": [],
                "count": 6,
                "total_pages": 2,
            },
            id="total_pagesを超えると空の記事一覧が取得できること",
        ),
        pytest.param(
            {
                "Authorization": f"Bearer {valid_access_token('6e2aa5a1-f792-47b8-9393-58fd657e7451')}"
            },
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
            {
                "Authorization": f"Bearer {valid_access_token('6e2aa5a1-f792-47b8-9393-58fd657e7451')}"
            },
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
def test_クエリパラメータ(headers: dict, query_params: dict, json_response: list[dict]):
    users = [
        db_models.User(
            id=uuid.UUID("6e2aa5a1-f792-47b8-9393-58fd657e7451"),
            name="sh-okada",
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
            user_id=uuid.UUID("6e2aa5a1-f792-47b8-9393-58fd657e7451"),
        ),
        db_models.Article(
            id=uuid.UUID("383853ee-a7b9-4792-aad8-aad82e5cc072"),
            title="記事3",
            text="# Hello World",
            published_at=datetime(2025, 7, 23, 3, 0, 0),
            user_id=uuid.UUID("6e2aa5a1-f792-47b8-9393-58fd657e7451"),
        ),
        db_models.Article(
            id=uuid.UUID("fbb7be33-bb8f-4ace-97af-8d711040dd99"),
            title="記事4",
            text="# Hello World",
            published_at=datetime(2025, 7, 23, 4, 0, 0),
            user_id=uuid.UUID("6e2aa5a1-f792-47b8-9393-58fd657e7451"),
        ),
        db_models.Article(
            id=uuid.UUID("6f027d9d-040c-4c51-a135-edff8b44c331"),
            title="記事5",
            text="# Hello World",
            published_at=datetime(2025, 7, 23, 5, 0, 0),
            user_id=uuid.UUID("6e2aa5a1-f792-47b8-9393-58fd657e7451"),
        ),
        db_models.Article(
            id=uuid.UUID("4e093992-8f3d-424d-8fda-733884197230"),
            title="記事6",
            text="# Hello World",
            published_at=datetime(2025, 7, 23, 6, 0, 0),
            user_id=uuid.UUID("6e2aa5a1-f792-47b8-9393-58fd657e7451"),
        ),
    ]

    session = next(get_mock_session())
    session.add_all(users + articles)
    session.commit()

    with freeze_time(datetime(2025, 7, 23, 0, 0, 0)):
        response = client.get(
            "/api/users/me/articles", headers=headers, params=query_params
        )

    assert response.json() == json_response
