# Руководство по работе с alembic

Скачать alembic (на машине один раз):
```
pip install alembic
```

Создать в проекте папки alembic:
```
alembic init alembic
```

Перед выполнением миграций должен быть пользователь posgres с нужным паролем и БД kolomna_hospital.

Создать новую версию (в кавычках пишем сообщение миграции):
```
alembic revision -m "create table diagnosises"
```
После этого создастся файл по пути alembic/versions. Можно заходить внутрь и изменять методы upgrade и downgrade.
Чтобы вставить отдельные sql-запросы, нужно использовать функцию op.execute.

Запустить миграции:
```
alembic upgrade head
```

Проверить крайнюю версию миграции:
```
alembic current
```

Посмотреть историю миграций:
```
alembic history --verbose
```

Откатить предыдущую миграцию:
```
alembic downgrade -1
```

Откатиться до конкретной предыдущей миграции:
```
alembic downgrade <revision_id>
```
