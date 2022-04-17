def test__on_get_show(client):
    result = client.simulate_get(path='/api/books/show', )

    assert len(result.json) == 2


def test__on_post_info(client):
    test_case = {
        'book_id': 628316291631,
    }

    result = client.simulate_post(
        path='/api/books/info',
        json=test_case,
    )

    excepted = {
        'id': 628316291631,
        'title': 'Scaling MongoDB',
        'subtitle': 'Sharding, Cluster Setup, and Administration',
        'authors': 'Kristina Chodorow',
        'publisher': "O'Reilly Media",
        'pages': 62,
        'year': 2011,
        'expire_date': 'Book is free for booking',
        'rating': 3,
        'desc': 'Create a MongoDB cluster that will to grow to meet the needs of your application.',
        'price': 16.99,
    }

    assert result.json == excepted


def test__on_post_book(client):
    auth_data = {
        'AUTHORIZATION': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImxvZ2luIjoiU3VwZXJEYW55YSIsIm5hbWUiOiJEYW55YSIsImdyb3VwIjoiVXNlciIsImVtYWlsIjoiZGFueWFAbWFpbC5ydSJ9.zlY_pU6vcCHp0qodcmOwiIArRvaAvDsroCPegP_ePW0',
    }

    test_case = {
        'book_id': 628316291631,
    }

    result = client.simulate_post(
        path='/api/books/book',
        headers=auth_data,
        json=test_case,
    )

    assert result.json == {'message': 'Book successfully booked'}


def test__on_post_active(client):
    auth_data = {
        'AUTHORIZATION': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImxvZ2luIjoiTWVnYU1pc2hhIiwibmFtZSI6Ik1pc2hhIiwiZ3JvdXAiOiJVc2VyIiwiZW1haWwiOiJtaXNoYUBtYWlsLnJ1In0.VY34hUc9FQREFUeVaKISudOPjhFvCVz5O6GKS2zO_gw',
    }

    result = client.simulate_post(
        path='/api/books/active',
        headers=auth_data,
        json={},
    )

    excepted = {
        'id': 628316291631,
        'title': 'Scaling MongoDB',
        'subtitle': 'Sharding, Cluster Setup, and Administration',
        'rating': 3,
        'price': 16.99,
    }

    assert result.json == excepted


def test__on_post_bought(client):
    auth_data = {
        'AUTHORIZATION': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImxvZ2luIjoiTWVnYU1pc2hhIiwibmFtZSI6Ik1pc2hhIiwiZ3JvdXAiOiJVc2VyIiwiZW1haWwiOiJtaXNoYUBtYWlsLnJ1In0.VY34hUc9FQREFUeVaKISudOPjhFvCVz5O6GKS2zO_gw',
    }

    result = client.simulate_post(
        path='/api/books/bought',
        headers=auth_data,
        json={},
    )

    excepted = {
        'id': 9781449303211,
        'title': 'Node.js, MongoDB and Angular Web Development, 2nd Edition',
        'subtitle': 'The definitive guide to using the MEAN stack to build web applications',
        'rating': 4,
        'price': 33.16,
    }

    assert result.json == [excepted]


def test__on_post_buy(client):
    auth_data = {
        'AUTHORIZATION': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImxvZ2luIjoiU3VwZXJEYW55YSIsIm5hbWUiOiJEYW55YSIsImdyb3VwIjoiVXNlciIsImVtYWlsIjoiZGFueWFAbWFpbC5ydSJ9.zlY_pU6vcCHp0qodcmOwiIArRvaAvDsroCPegP_ePW0',
    }

    test_case = {
        'book_id': 628316291631,
    }

    result = client.simulate_post(
        path='/api/books/buy',
        headers=auth_data,
        json=test_case,
    )

    assert result.json == {'message': 'Book successfully bought'}


def test__on_post_return(client):
    auth_data = {
        'AUTHORIZATION': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImxvZ2luIjoiU3VwZXJEYW55YSIsIm5hbWUiOiJEYW55YSIsImdyb3VwIjoiVXNlciIsImVtYWlsIjoiZGFueWFAbWFpbC5ydSJ9.zlY_pU6vcCHp0qodcmOwiIArRvaAvDsroCPegP_ePW0',
    }

    test_case = {
        'book_id': 628316291631,
    }

    result = client.simulate_post(
        path='/api/books/return',
        headers=auth_data,
        json=test_case,
    )

    assert result.json == {'message': 'Book successfully returned'}


def test__on_post_user_check(client):
    auth_data = {
        'AUTHORIZATION': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImxvZ2luIjoiU3VwZXJEYW55YSIsIm5hbWUiOiJEYW55YSIsImdyb3VwIjoiVXNlciIsImVtYWlsIjoiZGFueWFAbWFpbC5ydSJ9.zlY_pU6vcCHp0qodcmOwiIArRvaAvDsroCPegP_ePW0',
    }

    result = client.simulate_post(
        path='/api/books/user_check', headers=auth_data, json={}
    )

    assert len(result.json) == 1
