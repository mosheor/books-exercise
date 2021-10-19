# About

FRED (Flask + REact + Docker)

Tools and packages used in this project:

- [Flask](https://flask.palletsprojects.com/): a micro web framework written in Python
- [React](https://reactjs.org/): a JavaScript library for building user interfaces
- [Docker](https://www.docker.com/): a set of platform as a service products that uses OS-level virtualization to deliver software in packages called containers
- [Postgres](https://www.postgresql.org/): a free and open-source relational database management system
- [SQLAlchemy](https://www.sqlalchemy.org/): an open-source SQL toolkit and object-relational mapper for Python
- [Flask-RESTX](https://flask-restx.readthedocs.io/): a Flask extension for building REST APIs
- [PyTest](https://docs.pytest.org/en/latest/): a Python testing framework
- [Jest](https://jestjs.io/): a JavaScript testing framework

## Setup

You need to install the followings:

- Python 3
- Node.js
- Docker

## Run

1. Clone the repo in your mailbox
2. Switch to `fred` folder and run `docker-compose up -d --build`
3. Setup database and load data:
```
$ docker-compose exec backend python manage.py reset_db
$ docker-compose exec backend python manage.py load_data
```
4. Visit http://localhost:3007 to check the app (you can register a new user or use the sample testing user account username: test, email: test@test.com, password: test) 
5. Visit http://127.0.0.1:5001/docs/ to check API docs. 

## Tests

Run backend tests:

```
$ docker-compose exec backend python -m pytest "app/tests" -p no:warnings
```

Run frontend tests:

```
$ docker-compose exec frontend npm test
```

Access the database via psql:

```
$ docker-compose exec db psql -U postgres
# \c app_dev
# select * from user;
# select * from author;
# \q
```