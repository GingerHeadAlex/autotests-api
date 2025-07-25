import pytest

from clients.users.public_users_client import get_public_users_client
from clients.authentication.authentication_client import get_authentication_client, LoginRequestSchema,LoginResponseSchema
from clients.users.users_schema import CreateUserRequestSchema
from http import HTTPStatus
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.authentication import assert_login_response

@pytest.mark.regression
@pytest.mark.authentication
def test_login():
    public_users_client = get_public_users_client()
    request = CreateUserRequestSchema()
    # Создаем пользователя,не сохраняя результат в переменную
    public_users_client.create_user(request)

    # Берем email и password из запроса на создание пользователя и авторизуемся
    authentication_client = get_authentication_client()
    login_request = LoginRequestSchema(email=request.email, password=request.password)
    login_response = authentication_client.login_api(login_request)
    login_response_data = LoginResponseSchema.model_validate_json(login_response.text)

    # Проверка авторизации
    assert_status_code(login_response.status_code, HTTPStatus.OK)
    assert_login_response(login_response_data)
    validate_json_schema(login_response.json(), login_response_data.model_json_schema())

