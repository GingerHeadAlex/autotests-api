import httpx

from tools.fakers import fake

# Создаем пользователя
create_user_payload = {
    "email": fake.email(),
    "password": "string",
    "lastName": "string",
    "firstName": "string",
    "middleName": "string"
}
create_user_response = httpx.post("http://localhost:8000/api/v1/users", json = create_user_payload)
create_user_response_data = create_user_response.json()
print('Create user data:', create_user_response_data)

# Проходим аутентификацию
login_payload = {
    "email": create_user_payload['email'],
    "password": create_user_payload['password']
}
login_response = httpx.post("http://localhost:8000/api/v1/authentication/login", json = login_payload)
login_response_data = login_response.json()
print('Login data:', login_response_data)

# Обновляем пользователя

patch_user_payload = {
    "email": fake.email(),
    "lastName": "Testov",
    "firstName": "Test",
    "middleName": "Testovich"
}

patch_url = f'http://localhost:8000/api/v1/users/{create_user_response_data["user"]["id"]}'
patch_responce = httpx.patch(patch_url, json = patch_user_payload, headers= {'Authorization': f'Bearer {login_response_data["token"]["accessToken"]}'})
patch_responce_data = patch_responce.json()
print('Patch user data:', patch_responce_data)
