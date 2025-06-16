import socket  # Импортируем модуль socket для работы с сетевыми соединениями


def server():
    # Создаем список дл я хранения истории сообщений
    messages_history = []
    # Создаем TCP-сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Привязываем его к адресу и порту
    server_address = ('localhost', 12345)
    server_socket.bind(server_address)

    # Начинаем слушать входящие подключения (максимум 5 в очереди)
    server_socket.listen(10)
    print("Сервер запущен и ждет подключений...")

    while True:
        # Принимаем соединение от клиента
        client_socket, client_address = server_socket.accept()
        print(f"Пользователь с адресом: {client_address} подключился к серверу")

        # Получаем данные от клиента
        data = client_socket.recv(1024).decode()
        messages_history.append(data)
        print(f"Пользователь с адресом: {client_address} отправил сообщение: {data}")

        # Отправляем ответ клиенту
        response = f"Сервер получил: {messages_history}"
        client_socket.send('\n'.join(messages_history).encode())

        # Закрываем соединение с клиентом
        client_socket.close()


if __name__ == '__main__':
    server()