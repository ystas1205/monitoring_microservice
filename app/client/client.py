import requests


# Создание URL
response = requests.post(
    'http://127.0.0.1:5000/urls',
    json={
        "path": "https://www.google.ru/"},
    headers={"token": "0909a9c4-22ba-4a6b-8c17-e5d7e295402e"}

)
print(response.status_code)
print(response.json())

# response = requests.post(
#     'http://127.0.0.1:5000/users',
#     json={
#         "login": "ystas"
#     }
#
# )
# print(response.status_code)
# print(response.json())

# response = requests.post(
#     'http://127.0.0.1:5000/hello/world?name=John&age=28',
#     json={"key_1": "value_1", "key_2": "value_2"},
#     headers={"token": "secrets"},
# )
# print(response.status_code)
# print(response.json())

#
# response = requests.get(
#     'http://127.0.0.1:5000/urls',
#     headers={"token": "0909a9c4-22ba-4a6b-8c17-e5d7e295402e"}
#
# )
# print(response.status_code)
# print(response.json())


# response = requests.get(
#     "http://127.0.0.1:5000/events/dbb62795-70f4-47dc-86b5-523d103ef5bc?skip=0&limit=10",
#     headers={"token": "0909a9c4-22ba-4a6b-8c17-e5d7e295402e"})
#
# print(response.status_code)
# print(response.json())



# Удаление URL
# response = requests.delete(
#     'http://127.0.0.1:5000/urls/ae50b032-697a-407a-a8c3-98f5d6155114',
#     headers={"token": "0909a9c4-22ba-4a6b-8c17-e5d7e295402e"}
#
# )
# print(response.status_code)
# print(response.json())


# response = requests.get(
#     'http://127.0.0.1:5000/run-main',
#
#
# )
# print(response.status_code)
# print(response.json())
