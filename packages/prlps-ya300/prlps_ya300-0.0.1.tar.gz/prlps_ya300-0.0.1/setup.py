from setuptools import find_packages, setup

setup(
    name='prlps_ya300',
    version='0.0.1',
    author='prolapser',
    packages=find_packages(),
    url='https://github.com/gniloyprolaps/ya300',
    license='LICENSE.txt',
    description='получения содержания статей или видео с YouTube и запуска API-сервера для суммаризации через сервис 300.ya.ru',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    install_requires=['fastapi', 'pydantic', 'uvicorn', 'httpx'],
    python_requires='>=3.10',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)