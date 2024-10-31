import requests


#Создание URL
# response = requests.post(
#     'http://127.0.0.1:5000/urls',
#     json={
#         "path": "https://www.google.com/"},
#     headers={"token": "5dcdfca9-f9d6-422f-bbae-8aa2d843ffab"}
#
# )
# print(response.status_code)
# print(response.json())

# response = requests.post(
#     'http://127.0.0.1:5000/users',
#     json={
#         "login": "ystas"
#     }
#
# )
# print(response.status_code)
# print(response.json())
# print(response.text)



#
# response = requests.get(
#     'http://127.0.0.1:5001/urls',
#     headers={"token": "0909a9c4-22ba-4a6b-8c17-e5d7e295402e"}
#
# )
# print(response.status_code)
# print(response.json())


# response = requests.get(
#     "http://127.0.0.1:5000/events/8e80a309-8771-4664-9e85-2401d448dd21?skip=0&limit=10",
#     headers={"token": "5dcdfca9-f9d6-422f-bbae-8aa2d843ffab"})
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


# получение статистики мониторинга

response = requests.get(
    "http://127.0.0.1:5000/statistic?status_code=301&response_time=100,200&sort=created ",
    headers={"token": "5dcdfca9-f9d6-422f-bbae-8aa2d843ffab"})

print(response.status_code)
print(response.json())