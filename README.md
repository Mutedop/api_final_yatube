# **YaTube API**
> version 1.0 (v_1.0)
> * Версия 1.0 (далее v_1.0)


## Django _REST API_ project.
#### Project **Documentation**: http://localhost:8000/redoc/
* `Документация` проекта
_______
### Project installation.
* `Установка` проекта

##### 1. Установить виртуальное окружение 
`$ python -m venv venv`
##### 2. Установить зависимости 
`(venv) pip install -r requirements.txt`
##### 3. Создать и применить "миграции" 
`(venv) python manage.py makemigrations` -> `(venv) python manage.py migrate`
##### 4. Заупусить Django сервер 
`(venv) python manage.py runserver`
______

### Getting a Token
* Для получения `Token`
#### POST запрос на `http://localhost/api/v1/token/`
> потребуется ввести username/password
> Token Life Time: `7 days`
> Throttle: 'user': `10000/day, anon: 100/day`
