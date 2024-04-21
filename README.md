# Petpreneur

Сайт для объединения энтузиастов и единомышленников из разных сфер деятельности.
Например вы начинающий бэкенд разработчик, который хочет реализовать свою идею, но не может заплатить деньги за профессиональный фронтенд. Что же вам делать? Ответ прост: найти начинающего фронтендера, который тоже хочет сделать проект, но у которого нет средств на бэкенд разработчика. Именно эту возможность и должен предоставлять наш проект - соединять друг с другом единомышленников, для реализации своих идей, которые в будущем могут перерасти в стартап или огромную компанию.

## Технологии
- Python 3.11
- Django 4.2

# Установка 
## Клонирование репозитория
```
git clone https://gitlab.crja72.ru/django_2023/projects/petpreneur
```
## Создание виртуального окружения
### Для Linux
```
python3 -m venv venv
source venv/bin/activate
```
### Для Windows
```
python -m venv venv
venv\bin\activate
```
## Установка .env
### Для Linux
```
mv template.env .env
```
И измените .env под себя
### Для Windows
```
ren template.env .env
```
И измените .env под себя

## Установка requirements
### Выберите один из файлов
Для работы сайта:
```
pip install -r requirements/prod.txt
```
Для разработки:
```
pip install -r requirements/dev.txt
```
Для тестирования и отладки:
```
pip install -r requirements/test.txt
```

## Перейдите в директорию lyceum
```
cd petpreneur
```

# Подготовка проекта
1. Наполнить БД объектами
```
python manage.py migrate
python manage.py loaddata fixtures/data.json
```
2. Загрузить картинки из media
```
Нужно переименовать папку media_fixture в media*
```


# Запуск проекта
```
python manage.py runserver
```

### Уже созданные в фиктурах пользователи (Пароль test0000):

* ProjectGiver
* ProjectParticipator
* DummyUser1
* DummyUser2
* DummyUser3

### База данных
![DataBase](ER.jpeg)
