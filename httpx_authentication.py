import httpx  # Импортируем библиотеку HTTPX

# Инициализируем JSON-данные, которые будем отправлять в API
payload = {
    "email": "test@example.com",
    "password": "test"
}

# 1.Выполняем POST-запрос к эндпоинту /api/v1/authentication/login
request_post= httpx.post("http://localhost:8000/api/v1/authentication/login", json=payload)

# 2.Используя полученный accessToken, выполняем GET-запрос к эндпоинту /api/v1/users/me
response_post = request_post.json()
access_token = response_post['token']['accessToken']
request_get = httpx.get("http://localhost:8000/api/v1/users/me", headers={'Authorization': f'Bearer {access_token}'})
response_get = request_get.json()

# 3.Выведим в консоль JSON-ответ от сервера с данными о пользователе и статус код ответ
print(f'Ответ сервера: {response_get}')
print(f'Статус код: {request_get.status_code}')