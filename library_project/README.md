# **Проект по завершению буткемпа**

Проект представляет из себя набор из:

- двух `falcon` сервисов - `user_microservice` и `book_microservice`,
  построенных по `clean architecure` с соблюдением принципов `SOLID`;
- брокера сообщений `RabbitMQ`;
- `nginx` сервера;
- `SQL` базы (`PostgreSQL` СУБД).

Все микросервисы запускается в отдельных докер-контейнерах, и, за исключением `nginx`, конфигурируются посредством
передачи в `docker-compose.yml` переменных окружения для конкретного сервиса.

`falcon` сервисы подключаются к `PostgreSQL` БД, развернутых в `books_db` и `users_db` контейнерах соответственно.

Так как `book_microservice` и `user_microservice` должны читать сообщения из брокера, они имеют обработчиков событий,
поступаемых из брокера. Эти обработчики запускаются в отдельных docker контейнерах `books_api_consumer`
и `users_api_consumer` соответственно.

## **Краткое описание работы микросервисов**

### *nginx*

Используется для проксирования запросов к `falcon` сервисам. Его конфигурация находится в директории
*`library_project/components/nginx`* в файле *`nginx.conf`*. Слушает 1234 порт, поэтому все примеры запросов к
API будут идти через него.

### *RabbitMQ*

Брокер сообщений используется для взаимодействия между `falcon` сервисами.

- Переменные окружения
    - **RABBITMQ_DEFAULT_USER** - имя пользователя для подключения к RabbitMQ;
    - **RABBITMQ_DEFAULT_PASS** - пароль для подключения к RabbitMQ.

#### Пример взаимодействия:

`book_microservice` после добавления кинг в БД генерирует сообщение, которое в послествии отправляет
в `RabbitMQ`. `user_microservice` видит это событие, парсит его, и делает рассылку всем пользователям о лучших книгах
из числа добавленных.

### *PostgreSQL (Users DB)*

`PostgreSQL` СУБД, используемая `user_microservice`. При первом запуске создает 2 БД - основную,
используемую API в ходе работы, и тестовую, необходимую для запуска тестов.

- Переменные окружения
    - **POSTGRES_USER** - имя пользователя для подключения к PostgreSQL;
    - **POSTGRES_PASSWORD** - пароль для подключения к PostgreSQL.

### *PostgreSQL (Books DB)*

`PostgreSQL` СУБД, используемая `book_microservice`. При первом запуске создает 2 БД - основную,
используемую API в ходе работы, и тестовую, необходимую для запуска тестов.

- Переменные окружения
    - **POSTGRES_USER** - имя пользователя для подключения к PostgreSQL;
    - **POSTGRES_PASSWORD** - пароль для подключения к PostgreSQL.

### *user_microservice*

Сервис, взаимодействующий с сущностями пользователей - `Users`. В сервисе реализована логика для создания пользователя,
его авторизации, и осуществления рассылки сообщений. Пример http запросов - https://github.com/Korollayre/bootcamp_final_project/blob/master/library_project/components/user_microservice/docs/http_requests/users_api_requests.http

***HTTP API***

- Переменные окружения:
    - **DB_DRIVER** - диалект БД;
    - **DB_USER** - имя пользователя для подключения к БД;
    - **DB_PASSWORD** - пароль для подключения к БД;
    - **DB_HOST** - адрес хоста для подключения к БД;
    - **DB_PORT** - порт для подключения к БД;
    - **DB_DATABASE** - название основной базы БД;
    - **DB_TEST_DATABASE** - название тестовой базы БД;
    - **SECRET_JWT_KEY** - секретный ключ JWT-токена.

***Consumer***

- Переменные окружения:
    - **настройки HTTP API см. выше**
    - **RABBITMQ_HOST** - адрес хоста для подключения к RabbitMQ;
    - **RABBITMQ_PORT** - порт для подключения к RabbitMQ;
    - **RABBITMQ_USER** - имя пользователя для подключения к RabbitMQ;
    - **RABBITMQ_PASSWORD** - пароль для подключения к RabbitMQ.

### *book_microservice*

Сервис, взаимодействующий с сущностями книг - `Books`. В сервисе реализована логика для добавления книг в БД через cli
команду, получения списка книг (с фильтрами и без), получения полной информации по книге, бронирование, покупка, и
возврат книг, а так получение информации об текущей забронированной книге, получение истории бронирования, и получение
списка купленных книг. Пример http-запросов - https://github.com/Korollayre/bootcamp_final_project/blob/master/library_project/components/book_microservice/docs/http_requests/books_api_requests.http

***HTTP API***

- Переменные окружения:
    - **DB_DRIVER** - диалект БД;
    - **DB_USER** - имя пользователя для подключения к БД;
    - **DB_PASSWORD** - пароль для подключения к БД;
    - **DB_HOST** - адрес хоста для подключения к БД;
    - **DB_PORT** - порт для подключения к БД;
    - **DB_DATABASE** - название основной базы БД;
    - **DB_TEST_DATABASE** - название тестовой базы БД;
    - **SECRET_JWT_KEY** - секретный ключ JWT-токена.

***Consumer***

- Переменные окружения:
    - **настройки HTTP API см. выше**
    - **RABBITMQ_HOST** - адрес хоста для подключения к RabbitMQ;
    - **RABBITMQ_PORT** - порт для подключения к RabbitMQ;
    - **RABBITMQ_USER** - имя пользователя для подключения к RabbitMQ;
    - **RABBITMQ_PASSWORD** - пароль для подключения к RabbitMQ.

## **Локальное развертывание**

Для локального развертывания необходим `Docker` и `docker-compose`. Инструкция по установке `Docker` -
https://docs.docker.com/engine/install/,  `docker-compose` - https://docs.docker.com/compose/install/.
После установки компонентов необходимо в терминале перейти в директорию *`library_project/deployment`* и ввести команду
**docker-compose up --build**.

Для заполнения БД книг необходимо после запуска docker-compose файла ввести в терминале команду:

    docker exec -t deployment_books_api_1 bash -c "books_api init mongodb postgre mysql"

где **mongodb postgre mysql** - это теги, по которым будет осуществляться поиск и добавление книг в бд.

## **Тестирование**

Проект частично покрыт интеграционными и unit тестами.

Для запуска тестов `book_microservice` необходимо в терминале ввести команду:

    docker exec -t deployment_books_api_1 bash -c "python3 -m pytest --cov"

Для запуска тестов `user_microservice` необходимо в терминале ввести команду:

    docker exec -i deployment_users_api_1 bash -c "python3 -m pytest --cov"
