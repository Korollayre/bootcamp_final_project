FROM python:3.7-slim

WORKDIR /api

ENV PATH=$PATH:/usr/bin

COPY setup.py .
COPY setup.cfg .

RUN pip install --no-cache-dir --upgrade -e '.[dev]'

COPY dist ./dist

RUN pip install dist/*tar.gz

COPY ./entrypoint_*.sh /usr/bin/

RUN chmod +x /usr/bin/entrypoint_*.sh

COPY . .
