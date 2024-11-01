# Тестовое задание на позицию Python разработчик
_Перед началом работы необходимо сделать fork данной репозитории и продолжать работу в ней._

## Необходимо реализовать микросервис мониторинга доступности Web-ресурсов
Проверка доступности Web-ресурсов осуществляется путем выполнения запроса к ресурсу, и фиксации результатов ответа. На основе полученных результатов строится статистика по доступности узлов.

### Стек инструментов
Для реализации рекомендуем использовать следующий набор инструментов:
- flask
- flask-admin
- sqlalchemy
- postgresql
- alembic
Использование дополнительных средств приветствуется.

### Описание моделей и базы данных
Модели необходимо реализовать средствами sqlalchemy, в качестве базы данных использовать postgresql.
Для миграций рекомендуем использовать alembic.

Таблица `users` хранит информацию о пользователях сервиса  
```
<users>
* id
* token  | Токен доступа (для доступа к методам)
* created  | Дата создания записи
login  | Имя пользователя
```

Таблица `urls` хранит описание Web-ресурсов пользователя. Для списка данных ресурсов происходит мониторинг. 
```
<urls>
* id
* path  | Путь к Web-ресурсу
* created  | Дата создания записи
* user_id  | Идентификатор пользователя
title  | Название Web-ресурса
```

Таблица `events` хранит описание результатов запросов к Web-ресурсам. 
```
<events>
* id
* status_code  | Статус ответа
* url_id  | Идентификатор Web-ресурса
* response_time  | Время ответа
* created  | Дата создания записи
* response_size  | Размер ответа
active  | Флаг активности события (используется в методе delete)
```
Должна присутствовать начальная миграция реализованная средствами `Alembic`.
Управление данными необходимо реализовать через Flask-admin для таблицы `users`.

### Описание методов API:
Все методы должны отдавать ответ в формате `json`, в случае возникновения ошибок, ответы с сообщением об ошибке так же должны приходить в формате `json`.

Для доступа ко всем методам сделать проверку прав по токену пользователя (модель `user`), проверку реализовать в виде декоратора.
Токен передавать в заголовке.

#### /urls [GET]
_Список Web-ресурсов пользователя_
```
[
    {
        "id": ...,
        "path": "https://.....",
    },
    {
        "id": ...,
        "path": "https://.....",
    }
]
```

#### /urls [POST]
_Добавление url в мониторинг_


#### /urls/<url_id> [DELETE]
_Удаления url из мониторинга (делать неактивным)_


#### /events/<url_id>?skip=0&limit=10 [GET]
_Метод получения списка событий по url_

Параметры запроса:
- `skip`=0 - количество пропускаемых записей
- `limit`=10 - количество записей в ответе

```
{
    "items": {
        "url": ...,
        "created": ...,
        "response_time": ...,
        "status_code": ...
    },
    "items_total": 98
}
```

#### /statistic?status_code=301&response_time=100,200&sort=created [GET]
_Получения статистики мониторинга_

Параметры запроса:
- `status_code`=301 - код ответа события (необязательное)
- `response_time`=100,200 - диапазон времени ответа
- `sort`=created|response_time|status_code|response_size

##### Пример работы метода

В таблице `events` имеются следующие записи:
```
url_id                                   |  ...  |  response_time  |  status_code   |  response_size
11f895ed-89a9-487d-b110-0feb42dbe761     |       |  123            |  200           |  76237
11f895ed-89a9-487d-b110-0feb42dbe761     |       |  157            |  200           |  76237
11f895ed-89a9-487d-b110-0feb42dbe761     |       |  196            |  301           |  562
11f895ed-89a9-487d-b110-0feb42dbe761     |       |  83             |  200           |  76237
0feb42dd-89a9-487d-b110-ed0eb42d742d     |       |  450            |  200           |  67201
0feb42dd-89a9-487d-b110-ed0eb42d742d     |       |  392            |  200           |  67201
0feb42dd-89a9-487d-b110-ed0eb42d742d     |       |  1600           |  200           |  67201
0feb42dd-89a9-487d-b110-ed0eb42d742d     |       |  10050          |  500           |  278
0feb42dd-89a9-487d-b110-ed0eb42d742d     |       |  823            |  200           |  67921
```

Параметры фильтрации `status_code` и `response_time` отсеивают неподходящие под условия записи,
после чего происходит группировка по `url_id`, при группировке `response_time` вычисляется как среднее,
status_code как отношение 2..-х и 3..-х кодов к общему числу событий для данного url, `response_size` как максимальное значение,
created как последнее значение.
Результат сортируется в зависимости от параметра `sort`, например `created` (по возрастанию), `-created` (по убыванию).

Ответ метода с параметрами запроса `status_code=301&response_time=100,200&sort=created` должен выглядеть так:
```
[
    {
        "url_id": "11f895ed-89a9-487d-b110-0feb42dbe761",
        "avg_response_time": 196,
        "success_rate": 1.0,
        "max_response_size": 562
    }
]
```

### Мониторинг
Для мониторинга Web-ресурсов необходимо настроить `Celery` для выполнения периодических задач. 
Каждые 5 минут, воркер выбирает из базы все доступные `urls` и осуществляет http запрос к каждому из них, после чего фиксирует результаты в таблицу `events`. 

### Развертывание приложения
Необходимо подготовить файлы Dockerfile и docker-compose.yml для запуска приложения.
В результате запуск приложения должен осуществляться командой:

```
docker-compose up
