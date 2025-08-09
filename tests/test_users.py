from http import HTTPStatus

import pytest

from clients.users.public_users_client import PublicUsersClient
from clients.users.private_users_client import PrivateUsersClient
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema, GetUserResponseSchema
from clients.authentication.authentication_client import AuthenticationClient
from clients.authentication.authentication_schema import LoginRequestSchema
from tests.conftest import UserFixture
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.users import assert_create_user_response,assert_get_user_response


@pytest.mark.users
@pytest.mark.regression
def test_create_user(public_users_client: PublicUsersClient):
    request = CreateUserRequestSchema()
    response = public_users_client.create_user_api(request)
    response_data = CreateUserResponseSchema.model_validate_json(response.text)

    assert_status_code(response.status_code, HTTPStatus.OK)
    assert_create_user_response(request, response_data)

    validate_json_schema(response.json(), response_data.model_json_schema())



@pytest.mark.regression
@pytest.mark.authentication
def test_get_user_me(
        function_user: UserFixture,  # Используем фикстуру для создания пользователя
        authentication_client: AuthenticationClient,
        private_users_client: PrivateUsersClient
):
    # Запрашиваем текущего пользователя
    response_user_me = private_users_client.get_user_me_api()
    response_user_me_data = GetUserResponseSchema.model_validate_json(response_user_me.text)

    assert_status_code(response_user_me.status_code, HTTPStatus.OK)
    assert_get_user_response(response_user_me_data,function_user.response)

    validate_json_schema(response_user_me.json(), response_user_me_data.model_json_schema())

