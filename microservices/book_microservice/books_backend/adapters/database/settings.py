import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = f"{os.getenv('DB_DRIVER')}://" \
                  f"{os.getenv('DB_USER')}:" \
                  f"{os.getenv('DB_PASSWORD')}@" \
                  f"{os.getenv('DB_HOST')}:" \
                  f"{os.getenv('DB_PORT')}/" \
                  f"{os.getenv('DB_DATABASE')}"
