from sqlalchemy import create_engine, MetaData
from typing import Dict, Union
from os import PathLike
import json

from news_app.models import news, comments
from news_app.settings import load_config, BASE_DIR


DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"

ADMIN_DB_URL = DSN.format(
    user='postgres', password='postgres', database='postgres',
    host='localhost', port=5432
)

admin_engine = create_engine(ADMIN_DB_URL, isolation_level='AUTOCOMMIT')

USER_CONFIG = load_config()
USER_DB_URL = DSN.format(**USER_CONFIG['postgres'])
user_engine = create_engine(USER_DB_URL)


def load_sample_json_data(filename: Union[str, bytes, PathLike]) -> Dict:
    full_path = BASE_DIR / 'preset_data' / filename
    with open(full_path) as f:
        data = json.loads(f.read())
    return data


def setup_db(config):

    db_name = config['database']
    db_user = config['user']
    db_pass = config['password']

    conn = admin_engine.connect()
    conn.execute("DROP DATABASE IF EXISTS %s" % db_name)
    conn.execute("DROP ROLE IF EXISTS %s" % db_user)
    conn.execute("CREATE USER %s WITH PASSWORD '%s'" % (db_user, db_pass))
    conn.execute("CREATE DATABASE %s ENCODING 'UTF8'" % db_name)
    conn.execute("GRANT ALL PRIVILEGES ON DATABASE %s TO %s" %
                 (db_name, db_user))
    conn.close()


def teardown_db(config):

    db_name = config['database']
    db_user = config['user']

    conn = admin_engine.connect()
    conn.execute("""
      SELECT pg_terminate_backend(pg_stat_activity.pid)
      FROM pg_stat_activity
      WHERE pg_stat_activity.datname = '%s'
        AND pid <> pg_backend_pid();""" % db_name)
    conn.execute("DROP DATABASE IF EXISTS %s" % db_name)
    conn.execute("DROP ROLE IF EXISTS %s" % db_user)
    conn.close()


def create_tables(engine=user_engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[news, comments])


def sample_data(engine=user_engine):
    conn = engine.connect()
    news_data = load_sample_json_data('news.json')
    comments_data = load_sample_json_data('comments.json')
    conn.execute(news.insert(), news_data['news'])
    conn.execute(comments.insert(), comments_data['comments'])
    conn.close()


if __name__ == '__main__':
    setup_db(USER_CONFIG['postgres'])
    create_tables()
    sample_data()
