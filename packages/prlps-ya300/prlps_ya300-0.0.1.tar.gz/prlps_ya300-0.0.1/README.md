пакет предоставляет функции для получения содержания статей или видео с YouTube и запуска API-сервера для суммаризации через сервис 300.ya.ru. 

## установка

- из репозитория pypi:
`pip install prlps_ya300`

- из репозитория github:
`pip install git+https://github.com/gniloyprolaps/ya300.git`


## как использовать

### непосредственно в коде Python:

функция `get_summary` служит для получения содержания статьи или видео с YouTube.

#### аргументы:
- `article_or_youtube_url` (str): URL статьи или видео (поддерживаются только ссылки с YouTube).
- `short` (bool): возвратить только краткие заголовки тезисов для статей и только озаглавленные таймкоды для видео.
- `session_id` (str): `Session_id` из cookies с залогиненной страницы https://300.ya.ru.

#### возвращает:
- `str | None`: содержание статьи или видео в виде заголовков и тезисов или None, если возникли проблемы со ссылкой или авторизацией.

```python
import asyncio
from prlps_ya300 import get_summary  # импортируем функцию

# пример использования в асинхронном коде
async def main():
    session_id = "3:173323456.5.0.1724108495806:Y12iog:x21y.1.2:1|1141634570.0.2.3:1728003508|6:10200414.986812.uaRU96USIomXSkGPPOV1-Zov404"
    # получение содержания видео с YouTube:
    youtube_url = "https://www.youtube.com/watch?v=mloZU0LW8aQ"
    youtube_summary = await get_summary(youtube_url, short=False, session_id=session_id)
    print(youtube_summary)
    # получение озаглавленных таймкодов видео с YouTube:
    titled_timecodes = await get_summary(youtube_url, short=True, session_id=session_id)
    print(titled_timecodes)
    # получение содержания статьи:
    article_url = "https://azbyka.ru/otechnik/Ignatij_Brjanchaninov/simfonija-po-tvorenijam-svjatitelja-ignatija-brjanchaninova-tereshenko/3"
    article_summary = await get_summary(article_url, short=False, session_id=session_id)
    print(article_summary)
    # получение кратких тезисов статьи:
    article_url = "https://azbyka.ru/otechnik/Ignatij_Brjanchaninov/simfonija-po-tvorenijam-svjatitelja-ignatija-brjanchaninova-tereshenko/3"
    article_summary = await get_summary(article_url, short=True, session_id=session_id)
    print(article_summary)

asyncio.run(main())  # запуск асинхронного кода
```

### поднятие апи

функция `api_start` служит для запуска API-сервера FastAPI на указанном порту.

#### в коде:

```python
from prlps_ya300 import api_start  # импортируем функцию

api_start()  # запуск API-сервера
```

#### в консоли:
```bash
python -m prlps_ya300
```
или
```bash
python -c "from prlps_ya300 import api_start; api_start()"
```

#### запуск API-сервера через Docker:

```dockerfile
# базовый образ (вместо версии с alpine можно указать просто python:3.12):
FROM python:3.12-alpine
# установка библиотеки с апи:
RUN pip install --no-cache-dir --upgrade prlps_ya300
# уровень логирования, не обязательно:
ENV YA300_LOG_LEVEL=DEBUG
# порт, не обязательно (по умолчанию 7860):
ENV YA300_API_PORT=8080
# команда запуска апи:
CMD ["python", "-m", "prlps_ya300"]
```

#### выполнение запроса к API

##### через `curl`

```sh
curl -X GET "http://127.0.0.1:8000/summarize" -H "Content-Type: application/json" -d '{"url": "https://www.youtube.com/watch?v=mloZU0LW8aQ", "short": false, "session_id": "3:173323456.5.0.1724108495806:Y12iog:x21y.1.2:1|1141634570.0.2.3:1728003508|6:10200414.986812.uaRU96USIomXSkGPPOV1-Zov404"}'
```

##### в коде Python

```python
from httpx import AsyncClient

async def fetch_summary():
    async with AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:8000/summarize",
            json={"url": "https://www.youtube.com/watch?v=mloZU0LW8aQ", "short": False, "session_id": "3:173323456.5.0.1724108495806:Y12iog:x21y.1.2:1|1141634570.0.2.3:1728003508|6:10200414.986812.uaRU96USIomXSkGPPOV1-Zov404"}
        )
        print(response.json())

import asyncio
asyncio.run(fetch_summary())
```


## переменные окружения

### session_id для 300.ya.ru

необходимо указать `Session_id` из cookies с залогиненной страницы https://300.ya.ru.

задается в переменной окружения `YA300_SESSION_ID`:

```python
from os import environ
environ['YA300_SESSION_ID'] = '3:173323456.5.0.1724108495806:Y12iog:x21y.1.2:1|1141634570.0.2.3:1728003508|6:10200414.986812.uaRU96USIomXSkGPPOV1-Zov404'
```

в консоли:

```sh
export YA300_SESSION_ID='3:173323456.5.0.1724108495806:Y12iog:x21y.1.2:1|1141634570.0.2.3:1728003508|6:10200414.986812.uaRU96USIomXSkGPPOV1-Zov404'
```

### уровень логгирования (можно не указывать, по умолчанию INFO)

задается в переменной окружения `YA300_LOG_LEVEL`:

```python
from os import environ
environ['YA300_LOG_LEVEL'] = 'WARNING'
```

в консоли:

```sh
export YA300_LOG_LEVEL=DEBUG
```

### порт для API-сервера

задается в переменной окружения `YA300_API_PORT` (можно не указывать, по умолчанию 7860):

```python
from os import environ
environ['YA300_API_PORT'] = '8000'
```

в консоли:

```sh
export YA300_API_PORT=8000
```
