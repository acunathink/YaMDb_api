# api_yamdb


## Описание
Проект YaMDb собирает отзывы пользователей на произведения.
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Добавлять произведения, категории и жанры может только администратор.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка».
Пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку (от 1 до 10);
из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число).
Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

### Самостоятельная регистрация новых пользователей
Пользователь отправляет POST-запрос с параметрами `email` и `username` на эндпоинт `/api/v1/auth/signup/`.
Сервис YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на указанный адрес email.
Пользователь отправляет POST-запрос с параметрами `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит JWT-токен.
В результате пользователь может работать с API проекта, отправляя этот токен с каждым запросом.
После регистрации и получения токена пользователь может отправить PATCH-запрос на эндпоинт /api/v1/users/me/ и заполнить поля в своём профайле.


## Как запустить проект:

* Выполнить последовательно в командной строке:
  - Клонировать репозиторий:
    ```
    git clone https://github.com/acunathink/api_yamdb.git && cd api_yamdb
    ```

  - Cоздать виртуальное окружение:
    * <sub>linux/macos:</sub>
    ```
    python3 -m venv venv
    ```
    * <sub>windows:</sub>
    ```
    python -m venv venv
    ```

  - Aктивировать виртуальное окружение:
    * <sub>linux/macos:</sub>
    ```
    source venv/bin/activate
    ```
    * <sub>windows:</sub>
    ```
    source venv/scripts/activate
    ```

  - Установить зависимости из файла requirements.txt:
    ```
    pip install -r requirements.txt
    ```

  - Выполнить миграции и запустить проект:
    * <sub>linux/macos:</sub>
    ```
    cd api_yamdb && python3 manage.py migrate && python3 manage.py runserver
    ```

    * <sub>windows:</sub>
    ```
    cd api_yamdb && python manage.py migrate && python manage.py runserver
    ```

## Документация
* После запуска проекта документация доступна по адресу [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)
