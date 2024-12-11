from asyncio import sleep
from datetime import datetime
from re import compile, findall, search
from urllib.parse import urlparse
from os import environ
from httpx import AsyncClient, Timeout

from .log import set_logging

logger = set_logging(level=environ.get('YA300_LOG_LEVEL', 'info'))

YA300_URL = 'https://300.ya.ru/api/generation'
TIMEOUT = Timeout(connect=10.0, read=15.0, write=15.0, pool=10.0)


def extract_and_validate_url(text: str) -> str | None:
    url_pattern = compile(
        r'https?://'
        r'(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(),]|'
        r'%[0-9a-fA-F][0-9a-fA-F])+'
    )
    match = search(url_pattern, text)

    if match:
        url = match.group(0)
        parsed_url = urlparse(url)
        if parsed_url.scheme and parsed_url.netloc:
            return url
    return None


def extract_video_id(text: str) -> str | None:
    youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=|shorts/)?([^&=%\?]{11})'
    urls = findall(compile(youtube_regex), text)
    return [url[-1] for url in urls][0] if len(urls) > 1 else (urls[0][-1] if urls else None)


def ya_headers(session_id: str) -> dict[str, str]:
    match = search(r':(\d+)\.', session_id)
    yandex_csyr = match.group(1) if match else int(datetime.now().timestamp())
    return {
        'accept': '*/*',
        'content-type': 'application/json',
        'cookie': f'yandex_csyr={yandex_csyr}; Session_id={session_id}',
    }


def seconds_to_time_format(seconds: int) -> str:
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f'{hours:02}:{minutes:02}:{seconds:02}'


def parse_timecodes(ya_response: dict) -> str | None:
    title = ya_response.get('title')
    if not title:
        return None
    timecodes = [title]
    for keypoint in ya_response.get('keypoints', []):
        section = keypoint.get('content')
        start_time = keypoint.get('start_time')
        if section and start_time:
            timecodes.append(f'{section}: {seconds_to_time_format(start_time)}')
    return '\n'.join(timecodes)


def parse_summary(ya_response: dict, short: bool = False) -> str | None:
    title = ya_response.get('title')
    if not title:
        return None
    type_is_video = ya_response.get('type') == 'video'
    summary = [f"**{title}**"]
    if short:
        if type_is_video:
            return parse_timecodes(ya_response)
        for thesis in ya_response.get('thesis', []):
            theses_string = f'● {thesis.get("content")}'
            summary.append(theses_string)
        return '\n\n'.join(summary)
    for index, keypoint in enumerate(ya_response.get('keypoints' if type_is_video else 'chapters', []), start=1):
        section = keypoint.get('content', '')
        theses = keypoint.get('theses', [])
        theses_string = '\n'.join([f'● {thesis.get("content")}' for thesis in theses])
        summary.append(f'\n**{index}. {section}**\n{theses_string}')
    return '\n\n'.join(summary)


def payload(url: str) -> dict:
    yt_id = extract_video_id(url)
    if yt_id:
        return {'video_url': f'https://www.youtube.com/watch?v={yt_id}', 'type': 'video'}
    return {'article_url': url, 'type': 'article'}


async def fetch_ya300_summary(video_article_url: str, session_id: str) -> dict:
    video_article_url = extract_and_validate_url(video_article_url)
    logger.debug(f'video_article_url: {video_article_url}')
    if not video_article_url:
        return {'title': 'некорректная ссылка'}
    async with AsyncClient(headers=ya_headers(session_id), follow_redirects=True, timeout=TIMEOUT) as client:
        first_response = await client.post(YA300_URL, json=payload(video_article_url))
        logger.debug(f'first_response status: {first_response.status_code}')
        first_response.raise_for_status()
        first_response_data = first_response.json()
        logger.debug(f'first_response_data: {first_response_data}')
        session_id = first_response_data.get('session_id')
        poll_interval_ms = first_response_data.get('poll_interval_ms')
        status_code = first_response_data.get('status_code')
        if not session_id:
            if not poll_interval_ms:
                return {'title': 'некорректный источник'}
            return {'title': f'апи вернул status_code: {status_code}'}
        logger.debug(f'first_response_data.get("status_code"): {status_code}')
        if status_code > 1:
            error_code = first_response_data.get('error_code')
            return {'title': f'апи вернул error_code: {error_code}' if error_code else f'ошибка: status_code: {status_code}'}
        is_video = extract_video_id(video_article_url)
        second_payload = {'session_id': session_id, 'type': 'video' if is_video else 'article'}
        sharing_url = ''
        while not sharing_url:
            await sleep(poll_interval_ms / 1000)
            second_response = await client.post(YA300_URL, json=second_payload)
            second_response_json = second_response.json()
            error_code = second_response_json.get('error_code')
            if error_code:
                logger.error(f'error_code: {error_code}')
                return {'title': f'апи вернул error_code: {error_code}'}
            logger.debug(f'second_response status: {second_response.status_code}')
            status_code = second_response_json.get('status_code')
            logger.debug(f'second_response_data.get("status_code"): {status_code}')
            if is_video and status_code > 1:
                return {'title': f'апи вернул error_code: {error_code}' if error_code else f'ошибка: status_code: {status_code}'}
            poll_interval_ms = second_response_json.get('poll_interval_ms')
            sharing_url = second_response_json.get('sharing_url', '')
        logger.debug(f'second_response.json(): {second_response_json}')
        return second_response_json

async def get_summary(article_or_youtube_url: str, short: bool, session_id: str) -> str | None:
    """
    получить содержание статьи или видео с youtube.

    уровень логгирования задается в переменной окружения 'YA300_LOG_LEVEL'

    Args:
        article_or_youtube_url (str): URL статьи или видео (поддерживаются только ссылки с youtube).
        short (bool): возвратить только краткие заголовки тезисов для статей и только озаглавленные таймкоды для видео.
        session_id (str): `Session_id` из cookies с залогиненной страницы https://300.ya.ru.

    Returns:
        str | None: содержание статьи или видео в виде заголовков и тезисов или None, если возникли проблемы со ссылкой или авторизацией.
    """
    ya_response = await fetch_ya300_summary(article_or_youtube_url, session_id)
    if not ya_response:
        return None
    return parse_summary(ya_response, short=True if short else False)






