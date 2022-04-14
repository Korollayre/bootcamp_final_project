import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    BROKER_URL: str = f'amqp://' \
                      f"{os.getenv('RABBITMQ_USER')}:" \
                      f"{os.getenv('RABBITMQ_PASSWORD')}@" \
                      f"{os.getenv('RABBITMQ_HOST')}:" \
                      f"{os.getenv('RABBITMQ_PORT')}"
