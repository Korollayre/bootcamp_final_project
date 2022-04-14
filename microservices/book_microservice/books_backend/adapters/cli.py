import datetime
import threading

import click
import requests

from threading import Thread

from evraz.classic.messaging import Message, Publisher


def send_request(tag: str, publisher: Publisher, barrier, time: datetime):
    books_ids = []

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

        response['created_date'] = time

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

    barrier.wait()


def create_cli(publisher, MessageBus):
    @click.group()
    def cli():
        pass

    @cli.command()
    @click.argument('tags', nargs=-1, type=click.UNPROCESSED)
    def init(tags):
        barrier = threading.Barrier(len(tags) + 1)
        times = []
        for tag in tags:
            time = datetime.datetime.now()

            thread = Thread(target=send_request, args=(tag, publisher, barrier, time), daemon=False)
            thread.start()

            times.append(time)

        barrier.wait()

        publisher.publish(
            Message(
                'result',
                {
                    'api': 'books',
                    'action': 'send',
                    'data': {
                        'tags': tags,
                        'timestamps': times,
                    },
                }
            )
        )

    @cli.command()
    def consumer():
        MessageBus.declare_scheme()
        MessageBus.consumer.run()

    return cli
