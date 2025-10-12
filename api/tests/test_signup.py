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
    "request_body, status_code, json_response",
    [
        pytest.param(
            {"username": "ec-okada", "password": "Password123"},
            201,
            {"detail": "User created successfully."},
            id="ユーザー登録できること",
        ),
        pytest.param(
            {"username": "sh-okada", "password": "Password123"},
            400,
            {"detail": "Username is already in use."},
            id="ユーザー名は重複して登録できないこと",
        ),
        pytest.param(
            {"username": "a", "password": "Password123"},
            422,
            {
                "detail": [
                    {
                        "type": "string_too_short",
                        "loc": ["body", "username"],
                        "msg": "String should have at least 2 characters",
                        "input": "a",
                        "ctx": {"min_length": 2},
                    }
                ]
            },
            id="ユーザー名は1文字以下では登録できないこと",
        ),
        pytest.param(
            {"username": "123456789", "password": "Password123"},
            422,
            {
                "detail": [
                    {
                        "type": "string_too_long",
                        "loc": ["body", "username"],
                        "msg": "String should have at most 8 characters",
                        "input": "123456789",
                        "ctx": {"max_length": 8},
                    }
                ]
            },
            id="ユーザー名は9文字以上では登録できないこと",
        ),
        pytest.param(
            {"username": "ec@okada", "password": "Password123"},
            422,
            {
                "detail": [
                    {
                        "type": "string_pattern_mismatch",
                        "loc": ["body", "username"],
                        "msg": "String should match pattern '^[a-zA-Z0-9._-]+$'",
                        "input": "ec@okada",
                        "ctx": {"pattern": "^[a-zA-Z0-9._-]+$"},
                    }
                ]
            },
            id="半角英数字と記号（._-）以外の文字はユーザー名に含められないこと",
        ),
        pytest.param(
            {"username": "ec-okada", "password": "Pass123"},
            422,
            {
                "detail": [
                    {
                        "type": "too_short",
                        "loc": ["body", "password"],
                        "msg": "Value should have at least 8 items after validation, not 7",
                        "input": "Pass123",
                        "ctx": {
                            "field_type": "Value",
                            "min_length": 8,
                            "actual_length": 7,
                        },
                    }
                ]
            },
            id="パスワードは7文字以下では登録できないこと",
        ),
        pytest.param(
            {
                "username": "ec-okada",
                "password": "Password123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123",
            },
            422,
            {
                "detail": [
                    {
                        "type": "too_long",
                        "loc": ["body", "password"],
                        "msg": "Value should have at most 100 items after validation, not 101",
                        "input": "Password123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123",
                        "ctx": {
                            "field_type": "Value",
                            "max_length": 100,
                            "actual_length": 101,
                        },
                    }
                ]
            },
            id="パスワードは101文字以上では登録できないこと",
        ),
        pytest.param(
            {"username": "ec-okada", "password": "password123"},
            422,
            {
                "detail": [
                    {
                        "type": "value_error",
                        "loc": ["body", "password"],
                        "msg": "Value error, Password must contain at least one lowercase letter, one uppercase letter, and one digit",
                        "input": "password123",
                        "ctx": {"error": {}},
                    }
                ]
            },
            id="パスワードは半角英大文字を含める必要があること",
        ),
        pytest.param(
            {"username": "ec-okada", "password": "PASSWORD123"},
            422,
            {
                "detail": [
                    {
                        "type": "value_error",
                        "loc": ["body", "password"],
                        "msg": "Value error, Password must contain at least one lowercase letter, one uppercase letter, and one digit",
                        "input": "PASSWORD123",
                        "ctx": {"error": {}},
                    }
                ]
            },
            id="パスワードは半角英小文字を含める必要があること",
        ),
        pytest.param(
            {"username": "ec-okada", "password": "Password"},
            422,
            {
                "detail": [
                    {
                        "type": "value_error",
                        "loc": ["body", "password"],
                        "msg": "Value error, Password must contain at least one lowercase letter, one uppercase letter, and one digit",
                        "input": "Password",
                        "ctx": {"error": {}},
                    }
                ]
            },
            id="パスワードは数字を含める必要があること",
        ),
    ],
)
def test_レスポンス(request_body: dict, status_code: int, json_response: dict):
    user = db_models.User(
        id=uuid.UUID("5e3868cd-3ec0-4f86-9a94-84363c64da29"),
        name="sh-okada",
        password="$2b$12$ypi5a45bRgKPo4ZJk2IvQeqKJLlfpmGGwL9Pu9i/rEs2Pa0y7SywS",
    )

    session = next(get_mock_session())
    session.add(user)
    session.commit()

    with freeze_time(datetime(2025, 7, 23, 0, 0, 0)):
        response = client.post("/api/auth/signup", json=request_body)

    assert response.status_code == status_code
    assert response.json() == json_response
