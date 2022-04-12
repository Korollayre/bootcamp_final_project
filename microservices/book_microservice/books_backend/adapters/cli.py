import sys

import click
import requests

from evraz.classic.messaging import Message, Publisher
from evraz.classic.aspects import PointCut

from threading import Thread

join_points = PointCut()
join_point = join_points.join_point


@join_point
def send_request(tag: str, publisher: Publisher):
    books_ids = []
    print(publisher)
    response = requests.get(f'https://api.itbook.store/1.0/search/{tag}').json()

    total_books = int(response.get('total'))

    requests_number_for_books = total_books // 10 + int((total_books % 10) > 0)
    requests_number_for_books = requests_number_for_books if requests_number_for_books < 5 else 5

    for request_number in range(1, requests_number_for_books + 1):
        request_data = requests.get(f'https://api.itbook.store/1.0/search/{tag}/{request_number}').json()
        for book in request_data.get('books'):
            books_ids.append(book.get('isbn13'))

    for book_id in books_ids:
        response = requests.get(f'https://api.itbook.store/1.0/books/{book_id}').json()

        publisher.publish(
            Message(
                'result',
                {
                    'api': 'books',
                    'action': 'create',
                    'data': response,
                }
            )
        )

    sys.exit(0)


def create_cli(publisher):
    @click.group()
    def cli():
        pass

    @cli.command()
    @click.argument('tags', nargs=-1, type=click.UNPROCESSED)
    def init(tags):
        for tag in tags:
            thread = Thread(target=send_request, args=(tag, publisher), daemon=False)
            thread.start()

    return cli
