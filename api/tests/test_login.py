import pytest
from fastapi.testclient import TestClient

from app.infrastructure.db import db_models
from app.infrastructure.db.sqlite import get_mock_session
from app.main import app

client = TestClient(app)


class Test_ログイン:
    @pytest.fixture(autouse=True)
    def before_each(self):
        user = db_models.User(
            id="5e3868cd-3ec0-4f86-9a94-84363c64da29",
            name="sh-okada",
            password="$2b$12$ypi5a45bRgKPo4ZJk2IvQeqKJLlfpmGGwL9Pu9i/rEs2Pa0y7SywS",
        )

        session = next(get_mock_session())
        session.add(user)
        session.commit()

    @pytest.mark.parametrize(
        "username, password, status_code",
        [
            pytest.param(
                "sh-okada",
                "Password123",
                200,
                id="ユーザー名とパスワードが正しい場合",
            ),
            pytest.param(
                "bad-user",
                "Password123",
                400,
                id="ユーザー名が間違っている場合",
            ),
            pytest.param(
                "sh-okada",
                "BadPassword123",
                400,
                id="パスワードが間違っている場合",
            ),
        ],
    )
    def test_ステータスコード(self, username: str, password: str, status_code: int):
        response = client.post(
            "/api/auth/login", data={"username": username, "password": password}
        )

        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "username, password, json_response",
        [
            pytest.param(
                "sh-okada",
                "Password123",
                {
                    "id": "5e3868cd-3ec0-4f86-9a94-84363c64da29",
                    "username": "sh-okada",
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1ZTM4NjhjZC0zZWMwLTRmODYtOWE5NC04NDM2M2M2NGRhMjkiLCJleHAiOjE3NTM2NjI2MDB9.TlErX63YzBqw882C2jIMHFGmQY4ITuAgX-IAJX6QtA0",
                },
                id="ユーザー名とパスワードが正しい場合",
            ),
            pytest.param(
                "bad-user",
                "Password123",
                {"detail": "Bad Request"},
                id="ユーザー名が間違っている場合",
            ),
            pytest.param(
                "sh-okada",
                "BadPassword123",
                {"detail": "Bad Request"},
                id="パスワードが間違っている場合",
            ),
        ],
    )
    def test_JSONレスポンス(
        self, username: str, password: str, json_response: dict | None, freezer
    ):
        freezer.move_to("2025-07-28 00:00:00")
        response = client.post(
            "/api/auth/login", data={"username": username, "password": password}
        )

        assert response.json() == json_response
