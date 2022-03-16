NewsApp Test
=====

Example of polls project using aiohttp_, aiopg_ and aiohttp_jinja2_,
similar to Django one.

Install the app::

    $ pip install -r requirements.txt


Preparations

Create db and populate it with sample data::

    $ python init_db.py

Run
---
Run application:

    $ cd NewsApp
    $ python main.py

Open browser for read all news:

    http://localhost:8080/ 

Open browser for read news by id:

    http://localhost:8080/news/1

Tests
-----


    $ python -m unittest discover -s tests
