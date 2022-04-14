FROM python:3.7-slim

WORKDIR /api

ENV PATH=$PATH:/usr/bin

COPY ./components/book_microservice/setup.py .
COPY ./components/book_microservice/setup.cfg .

RUN pip install --no-cache-dir --upgrade -e '.[dev]'

COPY ./deployment/books_backend/dist ./dist

RUN pip install dist/*tar.gz

COPY ./deployment/books_backend/entrypoint_*.sh /usr/bin/

RUN chmod +x /usr/bin/entrypoint_*.sh

COPY ./components/book_microservice .
