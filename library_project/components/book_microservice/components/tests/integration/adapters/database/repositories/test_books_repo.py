import datetime

import pytest

from sqlalchemy.orm import registry

from books_backend.adapters.database import (
    tables,
    repositories,
)
from books_backend.application.entities import Books

created_date = datetime.datetime.now()


@pytest.fixture(scope='function')
def fill_books_table(session):
    books_data = [
        {
            "isbn13": 9781449314361,
            "title": "MongoDB and PHP",
            "subtitle": "Document-Oriented Data for Web Developers",
            "authors": "Steve Francia",
            "publisher": "O'Reilly Media",
            "pages": 78,
            "year": 2012,
            "rating": 3,
            "desc": "What would happen if you optimized a data store for the operations application developers actually use? You'd arrive at MongoDB, the reliable document-oriented database. With this concise guide, you'll learn how to build elegant database applications with MongoDB and PHP.Written by the Chief Solutio...",
            "price": 14.99,
            "created_date": created_date,
            "expire_date": None,
            "bought": False,
        },
        {
            "isbn13": 9781449326333,
            "title": "PostgreSQL: Up and Running",
            "subtitle": "A Practical Guide to the Advanced Open Source Database",
            "authors": "Regina Obe, Leo Hsu",
            "publisher": "O'Reilly Media",
            "pages": 166,
            "year": 2012,
            "rating": 4,
            "desc": "If you're thinking about migrating to the PostgreSQL open source database system, this guide provides a concise overview to help you quickly understand and use PostgreSQL's unique features. Not only will you learn about the enterprise class features in the 9.2 release, you'll also discover that Post...",
            "price": 19.95,
            "created_date": created_date,
            "expire_date": None,
            "bought": False,
        },
        {
            "isbn13": 9780470096000,
            "title": "PHP and MySQL For Dummies, 3rd Edition",
            "subtitle": "",
            "authors": "Janet Valade",
            "publisher": "Wiley",
            "pages": 456,
            "year": 2006,
            "rating": 4,
            "desc": "Been thinking of creating a high-quality interactive Web site? This book is just what you need to get started! Here's the fun and easy way(r) to develop a Web application in PHP 4, 5, or 6 and MySQL 5, test your software, enable your Web pages to display, change, and move database information, and m...",
            "price": 12.0,
            "created_date": created_date,
            "expire_date": created_date + datetime.timedelta(5),
            "bought": False,
        },
        {
            "isbn13": 9780132800754,
            "title": "MySQL, 4th Edition",
            "subtitle": "",
            "authors": "Paul Dubois",
            "publisher": "Addison-Wesley",
            "pages": 1224,
            "year": 2008,
            "rating": 0,
            "desc": "MySQL is an open source relational database management system that has experienced a phenomenal growth in popularity and use. Known for its speed and ease of use, MySQL has proven itself to be particularly well-suited for developing database-backed websites and applications.In MySQL, Paul DuBois pro...",
            "price": 0.0,
            "created_date": created_date,
            "expire_date": created_date - datetime.timedelta(2),
            "bought": False,
        },
        {
            "isbn13": 9781783989188,
            "title": "Learning PostgreSQL",
            "subtitle": "Create, develop and manage relational databases in real world applications using PostgreSQL",
            "authors": "Salahaldin Juba, Achim Vannahme, Andrey Volkov",
            "publisher": "Packt Publishing",
            "pages": 464,
            "year": 2015,
            "rating": 4,
            "desc": "PostgreSQL is one of the most powerful and easy to use database management systems. It has strong support from the community and is being actively developed with a new release every year. PostgreSQL supports the most advanced features included in SQL standards. Also it provides NoSQL capabilities, a...",
            "price": 31.51,
            "created_date": created_date,
            "expire_date": None,
            "bought": True,
        },
    ]

    session.execute(tables.books_table.insert(), books_data)


@pytest.fixture(scope='function')
def mapper():
    mapper = registry()
    mapper.map_imperatively(Books, tables.books_table)


@pytest.fixture(scope='function')
def books_repo(transaction_context):
    return repositories.BooksRepo(context=transaction_context)


def test__get_filtered_books(books_repo, fill_books_table):
    assert len(books_repo.get_filtered_books((), (), None)) == 4


def test__get_filtered_books__with_filters(books_repo, fill_books_table):
    assert len(
        books_repo.get_filtered_books(
            (('title', 'eq', 'MySQL, 4th Edition'), ), (), None
        )
    ) == 1


def test__get_by_id(books_repo, fill_books_table):
    test_case = {
        'book_id': 9781449326333,
    }

    assert books_repo.get_by_id(**test_case) is not None


def test__get_books_for_distribution(books_repo, fill_books_table):
    test_case = {
        'timestamp': created_date,
    }

    assert len(books_repo.get_books_for_distribution(**test_case)) == 3


def test__add_instance(books_repo, fill_books_table):
    test_case = {
        "isbn13": 92137902183320,
        "title": "MySQL, 1th Edition",
        "subtitle": "",
        "authors": "Paul Dubois",
        "publisher": "Addison-Wesley",
        "pages": 2341,
        "year": 2006,
        "rating": 2,
        "desc": "MySQL is an open source relational database management system that has experienced a phenomenal growth in popularity and use. Known for its speed and ease of use, MySQL has proven itself to be particularly well-suited for developing database-backed websites and applications.In MySQL, Paul DuBois pro...",
        "price": 0.0,
        "created_date": created_date,
        "expire_date": None,
        "bought": False,
    }

    assert books_repo.add_instance(Books(**test_case)) is None
