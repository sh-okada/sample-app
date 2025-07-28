import pytest
from fastapi.testclient import TestClient
from sqlmodel import select

from app.infrastructure.db import db_models
from app.infrastructure.db.sqlite import get_mock_session
from app.main import app
from app.shared import password

client = TestClient(app)


class Test_ユーザー登録:
    @pytest.mark.parametrize(
        "username, password, status_code",
        [
            pytest.param(
                "ec-okada",
                "Password123",
                201,
                id="正常に登録できる場合",
            ),
            pytest.param(
                "sh-okada",
                "Password123",
                400,
                id="ユーザー名がすでに存在する場合",
            ),
            pytest.param(
                "a",
                "Password123",
                422,
                id="ユーザー名が1文字以下の場合",
            ),
            pytest.param(
                "123456789",
                "Password123",
                422,
                id="ユーザー名が9文字以上の場合",
            ),
            pytest.param(
                "ec@okada",
                "Password123",
                422,
                id="半角英数字と記号（._-）以外の文字が含まれる場合",
            ),
            pytest.param(
                "ec-okada",
                "Pass123",
                422,
                id="パスワードが7文字以下の場合",
            ),
            pytest.param(
                "ec-okada",
                "Password123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123",
                422,
                id="パスワードが101文字以上の場合",
            ),
            pytest.param(
                "ec-okada",
                "password123",
                422,
                id="パスワードに半角英大文字が含まれない場合",
            ),
            pytest.param(
                "ec-okada",
                "PASSWORD123",
                422,
                id="パスワードに半角英小文字が含まれない場合",
            ),
            pytest.param(
                "ec-okada",
                "Password",
                422,
                id="パスワードに数字が含まれない場合",
            ),
        ],
    )
    def test_ステータスコード(self, username: str, password: str, status_code: int):
        user = db_models.User(
            id="5e3868cd-3ec0-4f86-9a94-84363c64da29",
            name="sh-okada",
            password="$2b$12$ypi5a45bRgKPo4ZJk2IvQeqKJLlfpmGGwL9Pu9i/rEs2Pa0y7SywS",
        )

        session = next(get_mock_session())
        session.add(user)
        session.commit()

        response = client.post(
            "/api/auth/signup", json={"username": username, "password": password}
        )

        assert response.status_code == status_code

    def test_パスワードはハッシュ化してDBに保存されること(self):
        client.post(
            "/api/auth/signup", json={"username": "sh-okada", "password": "Password123"}
        )

        session = next(get_mock_session())
        statement = select(db_models.User).where(
            db_models.User.name == "sh-okada",
        )
        user = session.exec(statement).one()

        assert password.verify_password("Password123", user.password)
