NewsApp Test
=====

Example of News read using aiohttp, aiopg and SQLAlchemy.


How to deploy in docker compose.

Build docker with web application:

    $ docker build -f Dockerfile -t test:newsapp .

At the first launch, you need to create a table and test data:

    $ docker-compose up -d db
    $ python init_db.py
    $ docker-compose dowb


Run
---
Run application:

    $ docker-compose up

Open browser for read all news:

    http://127.0.0.1:8080/

For read news by id:

    http://127.0.0.1:8080/news/1


Stop
---
Stop application:

    $ docker-compose down

Tests in web container
-----

    $ docker-compose exec web python -m unittest discover -s tests
