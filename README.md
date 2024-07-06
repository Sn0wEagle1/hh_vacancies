1. Установка и запуск приложения 
1.1. Системные требования
Операционная система: Windows, macOS, Linux;
Python: версии 3.x;
PostgreSQL: установленный и настроенный сервер базы данных

1.2. Установка необходимых компонентов
Установите Python:
Загрузите и установите Python с официального сайта: python.org.

Установите PostgreSQL:
Загрузите и установите PostgreSQL с официального сайта: postgresql.org.

1.3. Клонирование репозитория
Клонируйте репозиторий с кодом проекта.
Используйте команду:
```
git clone https://github.com/Sn0wEagle1/hh_vacancies
```
Перейдите в директорию проекта:
```
cd job_portal
```

1.4. Установка зависимостей
Установите зависимости:
Выполните команду:
```
pip install -r requirements.txt
```

1.5. Настройка базы данных
Создайте базу данных в PostgreSQL:
Создайте новую базу данных и пользователя.

Настройте подключение к базе данных в Django:
Откройте файл settings.py и укажите параметры подключения:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ваша_база_данных',
        'USER': 'ваш_пользователь',
        'PASSWORD': 'ваш_пароль',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

1.6. Применение миграций
Примените миграции:
Выполните команду:
```
python manage.py migrate
```
После этого вам нужно запустить parser.py, чтобы данные с hh.ru спарсились в базу данных  (в parser.py можно поменять ключевые слова в PARAMS, по которым изначально парсятся данные)

1.7. Запуск локального сервера
Запустите локальный сервер:
```
python manage.py runserver
```
2. Использование приложения
   
2.1. Регистрация и вход
Регистрация:
Перейдите на страницу регистрации и создайте новую учетную запись, заполнив необходимые поля.
Вход:
Перейдите на страницу входа и войдите в систему, используя свои учетные данные.

2.2. Основные функции
Просмотр данных:
Перейдите на главную страницу, чтобы просмотреть основную информацию и данные, предоставляемые приложением.
Сохранение вакансий:
Около каждой вакансии есть кнопка "Сохранить", при нажатии на которую, она сохранится у вас в профиле.
Удаление записей:
В профиле у каждой вакансии есть кнопка "Удалить", при нажатии на которую, вакансия удалится из сохраненных вами.
