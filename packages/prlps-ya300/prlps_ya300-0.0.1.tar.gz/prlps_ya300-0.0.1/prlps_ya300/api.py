from contextlib import asynccontextmanager
from os import environ
from re import match
from typing import AsyncGenerator, Optional

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from uvicorn import run as uvicorn_run

from .utils import extract_and_validate_url, get_summary, logger

logger.info('инициализация приложения...')


class YaRequest(BaseModel):
    url: str
    short: Optional[bool] = False
    session_id: Optional[str] = None


class YaResponse(BaseModel):
    content: Optional[str] = None
    error: Optional[str] = None


def validate_session_id(session_id: str) -> bool:
    pattern = r'^\d+:\d+\.\d+\.\d+\.\d+:[\w-]+:[\w-]+\.\d+\.\d+:\d+\|\d+\.\d+\.\d+\.\d+:\d+\|\d+:\d+\.\d+\.[\w-]+$'
    return bool(match(pattern, session_id))


def convert_port(port_str: str) -> int | None:
    port_str = str(port_str).strip()
    if not port_str.isdigit() or not 1 <= len(port_str) <= 5:
        return None
    port = int(port_str)
    if not 1 <= port <= 65535:
        return None

    return port


@asynccontextmanager
async def app_lifespan(_) -> AsyncGenerator:
    logger.info('запуск приложения')
    try:
        logger.info('старт API')
        yield
    finally:
        logger.info('приложение завершено')


app = FastAPI(
    lifespan=app_lifespan,
    title='YA300_API',
    description='API для получения кратких пересказов статей и видео с youtube.',
    version='0.0.1',
    license_info={
        'name': 'MIT License',
        'url': 'https://opensource.org/licenses/MIT',
    },

)


@app.get('/', include_in_schema=False)
async def root():
    return get_swagger_ui_html(
        openapi_url="/openapi.json", title="YA300_API",
        swagger_favicon_url='https://yastatic.net/s3/distribution/stardust/browser-summary-web/static/favicon.png',
        swagger_ui_parameters={
            'defaultModelsExpandDepth': -1,
            'defaultModelExpandDepth': 2,
            'docExpansion': 'full',
            'syntaxHighlight': True,
        },
    )


@app.post('/summarize', response_model=YaResponse)
async def summarize(request: YaRequest):
    """
    основной эндпоинт для суммаризации

    Args:
        request (YaRequest): входные данные в формате JSON: {"url": "str", "short": "bool (optional)", "session_id": "str (optional)"}.

    Returns:
        dict: ответ с содержанием статьи или видео или сообщением об ошибке.
    """
    # Пример обработки данных
    url = request.url
    short = request.short
    session_id = str(request.session_id or environ.get('YA300_SESSION_ID'))
    error = []
    if not validate_session_id(session_id):
        error.append(
            'невалидный Session_id! он должен быть в формате `3:173323456.5.0.1724108495806:Y12iog:x21y.1.2:1|1141634570.0.2.3:1728003508|6:10200414.986812.uaRU96USIomXSkGPPOV1-Zov404`')
    if not url or not extract_and_validate_url(url):
        error.append('некорректная ссылка')
    if short and not isinstance(short, bool):
        error.append('некорректное значение short')
    if error:
        error.append("входные данные должны быть в формате JSON: {'url': 'str', 'short': 'bool (optional)', 'session_id': 'str (optional)'}")
        error_msg = '\n'.join(error)
        return JSONResponse(content={'content': None, 'error': error_msg}, status_code=400)

    answer = await get_summary(url, short, session_id)

    return JSONResponse(content={'content': answer, 'error': None}, status_code=200)


def api_start():
    """
    запускает сервер FastAPI на указанном порту в переменной окружения `YA300_API_PORT`, порт по умолчанию 7860.
    уровень логгирования задается в переменной окружения 'YA300_LOG_LEVEL'.
    основной эндпоинт для суммаризации: `/summarize`.
    ожидает get-запросы в формате JSON: {"url": "str", "short": "bool (optional)", "session_id": "str (optional)"}
    """
    port = convert_port(environ.get('YA300_API_PORT', '7860'))
    logger.critical('запуск сервера на: http://127.0.0.1:%s', port)
    uvicorn_run(app, host='0.0.0.0', port=port, log_level='info')

