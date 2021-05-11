# Employee catalog


## Dependencies
The base project dependencies:

- docker
- python version 3.8 +
- django 3.2.2
- PostgreSQL 
- djangorestframework 3.12.4
- redis
- celery

The complete list of dependencies can be found at backend/requirements-dev.txt.
For using API firstly create user and then get access key in swagger ui.
You can fill db with test data and use email: lead@mail.ru, pass: lead to login as superuser.
## Usage
Create 2 files in main folder:
.env.dev 
```
DEBUG=1
DJANGO_ALLOWED_HOSTS=*
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=django_dev
SQL_USER=django
SQL_PASSWORD=django_pass
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres

```

.env.db
```
POSTGRES_USER=django
POSTGRES_PASSWORD=django_pass
POSTGRES_DB=django_dev
```
Update the file permissions locally:
```
$ chmod +x entrypoint.sh
```

### Development:
```
# Up
$ make build-dev

# Navigate to:
# - admin http://0.0.0.0:8080/admin/
# - api (swagger) http://0.0.0.0:8080/api/schema/swagger-ui/#/


# Logs
$ make logs-dev

# Down
$ make stop-dev

# Create superuser
$ create-admin-dev

# Fill db with fake data
$ fill-db-dev

```
---
