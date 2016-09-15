FROM python:3.5

RUN pip install aiohttp
RUN pip install docker-py

COPY /src /src

WORKDIR /src
CMD ./run.sh
