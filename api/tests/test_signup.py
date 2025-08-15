import pytest
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from app.infrastructure.db import db_models
from app.infrastructure.db.sqlite import get_mock_session
from app.main import app
from tests.conftest import MockUUID

client = TestClient(app)


@pytest.fixture(autouse=True)
def before_each():
    user = db_models.User(
        id="5e3868cd-3ec0-4f86-9a94-84363c64da29",
        name="sh-okada",
        password="$2b$12$ypi5a45bRgKPo4ZJk2IvQeqKJLlfpmGGwL9Pu9i/rEs2Pa0y7SywS",
    )

    session = next(get_mock_session())
    session.add(user)
    session.commit()


@pytest.mark.parametrize(
    "request_body, status_code",
    [
        pytest.param(
            {"username": "ec-okada", "password": "Password123"},
            201,
            id="正常に登録できる場合",
        ),
        pytest.param(
            {"username": "sh-okada", "password": "Password123"},
            400,
            id="ユーザー名がすでに存在する場合",
        ),
        pytest.param(
            {"username": "a", "password": "Password123"},
            422,
            id="ユーザー名が1文字以下の場合",
        ),
        pytest.param(
            {"username": "123456789", "password": "Password123"},
            422,
            id="ユーザー名が9文字以上の場合",
        ),
        pytest.param(
            {"username": "ec@okada", "password": "Password123"},
            422,
            id="半角英数字と記号（._-）以外の文字が含まれる場合",
        ),
        pytest.param(
            {"username": "ec@okada", "password": "Password123"},
            422,
            id="半角英数字と記号（._-）以外の文字が含まれる場合",
        ),
        pytest.param(
            {"username": "ec-okada", "password": "Pass123"},
            422,
            id="パスワードが7文字以下の場合",
        ),
        pytest.param(
            {
                "username": "ec-okada",
                "password": "Password123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123",
            },
            422,
            id="パスワードが101文字以上の場合",
        ),
        pytest.param(
            {"username": "ec-okada", "password": "password123"},
            422,
            id="パスワードに半角英大文字が含まれない場合",
        ),
        pytest.param(
            {
                "username": "ec-okada",
                "password": "Password123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123",
            },
            422,
            id="パスワードが101文字以上の場合",
        ),
        pytest.param(
            {"username": "ec-okada", "password": "password123"},
            422,
            id="パスワードに半角英大文字が含まれない場合",
        ),
        pytest.param(
            {"username": "ec-okada", "password": "PASSWORD123"},
            422,
            id="パスワードに半角英小文字が含まれない場合",
        ),
        pytest.param(
            {"username": "ec-okada", "password": "Password"},
            422,
            id="パスワードに数字が含まれない場合",
        ),
    ],
)
def test_ステータスコード(request_body: dict, status_code: int):
    response = client.post("/api/auth/signup", json=request_body)

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "request_body, result",
    [
        pytest.param(
            {"username": "ec-okada", "password": "Password123"},
            db_models.User(
                id="a5c28c8f-1b99-4d72-924f-d46619c1a1cb",
                name="ec-okada",
                password="$2b$12$wmu2fDI2jcijH/jbs4fL.ehlg7bIb0uA1JarTqDiagc9dQbXbAwMy",
            ),
            id="正常に登録できる場合",
        ),
        pytest.param(
            {"username": "sh-okada", "password": "Password123"},
            None,
            id="ユーザー名がすでに存在する場合",
        ),
        pytest.param(
            {"username": "a", "password": "Password123"},
            None,
            id="ユーザー名が1文字以下の場合",
        ),
        pytest.param(
            {"username": "123456789", "password": "Password123"},
            None,
            id="ユーザー名が9文字以上の場合",
        ),
        pytest.param(
            {"username": "ec@okada", "password": "Password123"},
            None,
            id="半角英数字と記号（._-）以外の文字が含まれる場合",
        ),
        pytest.param(
            {"username": "ec-okada", "password": "Pass123"},
            None,
            id="パスワードが7文字以下の場合",
        ),
        pytest.param(
            {
                "username": "ec-okada",
                "password": "Password123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123",
            },
            None,
            id="パスワードが101文字以上の場合",
        ),
        pytest.param(
            {"username": "ec-okada", "password": "password123"},
            None,
            id="パスワードに半角英大文字が含まれない場合",
        ),
        pytest.param(
            {"username": "ec-okada", "password": "PASSWORD123"},
            None,
            id="パスワードに半角英小文字が含まれない場合",
        ),
        pytest.param(
            {"username": "ec-okada", "password": "Password"},
            None,
            id="パスワードに数字が含まれない場合",
        ),
    ],
)
def test_DB登録内容(
    request_body: dict,
    result: db_models.User,
    mocker: MockerFixture,
    mock_uuid: MockUUID,
):
    mock_uuid(
        db_models.User,
        db_models.User.model_fields["id"],
        "a5c28c8f-1b99-4d72-924f-d46619c1a1cb",
    )
    mocker.patch(
        "app.shared.password.get_password_hash",
        return_value="$2b$12$wmu2fDI2jcijH/jbs4fL.ehlg7bIb0uA1JarTqDiagc9dQbXbAwMy",
    )
    client.post("/api/auth/signup", json=request_body)

    session = next(get_mock_session())
    user = session.get(db_models.User, "a5c28c8f-1b99-4d72-924f-d46619c1a1cb")

    assert user == result
