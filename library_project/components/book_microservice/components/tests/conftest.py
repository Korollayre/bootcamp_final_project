from datetime import datetime, timedelta

import pytest

from books_backend.application import entities


@pytest.fixture
def book_1():
    return entities.Books(
        isbn13=628316291631,
        title="Scaling MongoDB",
        subtitle="Sharding, Cluster Setup, and Administration",
        authors="Kristina Chodorow",
        publisher="O'Reilly Media",
        pages=62,
        year=2011,
        rating=3,
        desc=
        "Create a MongoDB cluster that will to grow to meet the needs of your application.",
        price=16.99,
        created_date='2022-04-22 07:47:20',
        expire_date=None,
        bought=False,
    )


@pytest.fixture
def book_2():
    return entities.Books(
        isbn13=9781449303211,
        title="Node.js, MongoDB and Angular Web Development, 2nd Edition",
        subtitle=
        "The definitive guide to using the MEAN stack to build web applications",
        authors="Brad Dayley, Brendan Dayley, Caleb Dayley",
        publisher="Addison-Wesley",
        pages=640,
        year=2017,
        rating=4,
        desc=
        "Node.js is a leading server-side programming environment, MongoDB is the most popular NoSQL database.",
        price=33.16,
        created_date='2022-04-22 07:47:20',
        expire_date=None,
        bought=False,
    )


@pytest.fixture
def booked_book():
    return entities.Books(
        isbn13=628316291631,
        title="Scaling MongoDB",
        subtitle="Sharding, Cluster Setup, and Administration",
        authors="Kristina Chodorow",
        publisher="O'Reilly Media",
        pages=62,
        year=2011,
        rating=3,
        desc=
        "Create a MongoDB cluster that will to grow to meet the needs of your application.",
        price=16.99,
        created_date='2022-04-22 07:47:20',
        expire_date=datetime.today() + timedelta(7),
        bought=False,
    )


@pytest.fixture
def bought_book():
    return entities.Books(
        isbn13=9781449303211,
        title="Node.js, MongoDB and Angular Web Development, 2nd Edition",
        subtitle=
        "The definitive guide to using the MEAN stack to build web applications",
        authors="Brad Dayley, Brendan Dayley, Caleb Dayley",
        publisher="Addison-Wesley",
        pages=640,
        year=2017,
        rating=4,
        desc=
        "Node.js is a leading server-side programming environment, MongoDB is the most popular NoSQL database.",
        price=33.16,
        created_date='2022-04-22 07:47:20',
        expire_date=None,
        bought=True,
    )


@pytest.fixture
def book_history_1(book_1):
    book_history_1 = entities.BooksHistory(
        id=1,
        book_id=9781449303211,
        user_id=1,
        created_date='2022-04-15 12:47:20',
    )

    book_history_1.book = book_1

    return book_history_1


@pytest.fixture
def book_history_2(book_2):
    book_history_2 = entities.BooksHistory(
        id=2,
        book_id=32138723091,
        user_id=2,
        created_date='2022-04-15 12:48:45',
    )

    book_history_2.book = book_2

    return book_history_2


@pytest.fixture
def book_history_with_booked_book(booked_book):
    book_history_with_booked_book = entities.BooksHistory(
        id=1,
        book_id=9781449303211,
        user_id=1,
        created_date='2022-04-15 12:47:20',
    )

    book_history_with_booked_book.book = booked_book

    return book_history_with_booked_book


@pytest.fixture
def book_history_with_bought_book(bought_book):
    book_history_with_bought_book = entities.BooksHistory(
        id=2,
        book_id=32138723091,
        user_id=2,
        created_date='2022-04-15 12:48:45',
    )

    book_history_with_bought_book.book = bought_book

    return book_history_with_bought_book
