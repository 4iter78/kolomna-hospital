# Приложение kolomna-hospital
Репозиторий для информационной системы ГБУЗ Московской области "Коломенская больница".
# Подключение к БД
Для подключения к БД нужно заполнить локальный файл .env в корне проекта и указать в нём свои данные для подключения:
```commandline
DB_HOST=postgres
DB_PORT=5432
DB_NAME=kolomna_hospital
DB_USER=myuser
DB_PASSWORD=secret
```
# Запуск БД из docker-compose.yaml по пути /docker
```commandline
docker compose up -d
```
