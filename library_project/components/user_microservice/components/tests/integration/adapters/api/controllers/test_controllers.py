import json


def test__on_post_register(client, user):
    test_case = {
        'login': 'SuperDanya',
        'email': 'danya@mail.ru',
        'password': 'password',
        'name': 'Danya',
    }

    test_case_bytes = json.dumps(test_case)

    result = client.simulate_post(
        path='/api/users/register',
        body=test_case_bytes
    )

    assert result.json == {'message': 'User registration completed successfully'}


def test__on_post_login(client, user):
    test_case = {
        'email': 'danya@mail.ru',
        'password': 'password',
    }

    test_case_bytes = json.dumps(test_case)

    result = client.simulate_post(
        path='/api/users/login',
        body=test_case_bytes
    )

    assert result.json == {'message': 'Login complete successful'}


def test__on_get_logout(client, user):
    test_case = {
        'AUTHORIZATION': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImxvZ2luIjoiU3VwZXJEYW55YSIsIm5hbWUiOiJEYW55YSIsImdyb3VwIjoiVXNlciIsImVtYWlsIjoiZGFueWFAbWFpbC5ydSJ9.zlY_pU6vcCHp0qodcmOwiIArRvaAvDsroCPegP_ePW0',
    }

    result = client.simulate_get(
        path='/api/users/logout',
        headers=test_case
    )

    assert result.json == {'message': 'Logout complete successful'}


def test__on_get_show_user(client, user):
    test_case = {
        'AUTHORIZATION': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImxvZ2luIjoiU3VwZXJEYW55YSIsIm5hbWUiOiJEYW55YSIsImdyb3VwIjoiVXNlciIsImVtYWlsIjoiZGFueWFAbWFpbC5ydSJ9.zlY_pU6vcCHp0qodcmOwiIArRvaAvDsroCPegP_ePW0',
    }

    result = client.simulate_get(
        path='/api/users/show_user',
        headers=test_case
    )

    excepted = {
        'login': 'SuperDanya',
        'email': 'danya@mail.ru',
        'name': 'Danya',
        'age': None,
    }

    assert result.json == excepted
