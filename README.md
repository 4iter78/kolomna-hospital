# Приложение kolomna-hospital
Репозиторий для информационной системы Медицинский склад ГБУЗ Московской области "Коломенская больница".
# Подключение к БД
Для подключения к БД и разворачивания приложения нужно заполнить локальный файл .env в корне проекта, такой же положить в /docker 
и указать в нём свои данные для подключения:
```commandline
DB_HOST=postgres
DB_PORT=5432
DB_NAME=kolomna_hospital
DB_USER=myuser
DB_PASSWORD=secret
APP_PORT=8001
```
# Перед запуском создать requirements.txt, если его нет
```commandline
    python -m pip freeze > requirements.txt
```
# Запуск БД из docker-compose.yaml по пути /docker
```commandline
    docker compose up -d
```
# Посмотреть контейнеры
```commandline
    docker ps
```
# Запуск отдельно только приложения, без БД
```commandline
    docker compose up -d app
```
