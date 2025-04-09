# Онлайн-платформа для обзоров и оценок медиа-контента.
Авторы: Похлебкина Елизавета, Воробьев Василий, Анастасия Давыдова  
Проект MediaRate собирает отзывы пользователей на произведения.  
Произведения делятся на категории. Пользователи могут ставить оценки произведениям и оставлять  
свои комментарии к чужим отзывам. 

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/aftergl0wn/MediaRate.git
```

```
cd MediaRate
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```


## Какие технологии и пакеты использовались:
requests==2.26.0  
Django==3.2  
djangorestframework==3.12.4  
PyJWT==2.1.0  
pytest==6.2.4  
pytest-django==4.4.0  
pytest-pythonpath==0.7.3  

### Пример POST-запроса с правами доступа администратора:
POST ...api/v1/categories/
Пример запроса: 
```
{
  "name": "Film",
  "slug": "film"
}
```
Пример удачного выполнения запроса: 

```
{
  "name": "Film",
  "slug": "film"
}
```
Пример ошибки 401: 

```
{
    "detail": "Учетные данные не были предоставлены."
}
```

### Как импортировать данные из csv таблиц:

Пример импорта category.csv: 

```
python3 manage.py import_data_category D:/Dev/MediaRate/MediaRate/static/data/category.csv
```
При удачном выполнение вывод в терминале будет: 

```
Data category.csv imported successfully
```
