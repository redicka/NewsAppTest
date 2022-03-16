import os
import aiopg.sa
from typing import List, Dict
import datetime

from aiopg.sa.result import ResultProxy
from sqlalchemy.sql.expression import label

from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, DateTime, Text, Boolean, and_, func, select,
)

__all__ = ['news', 'comments']

meta = MetaData()


news = Table('news', meta,
    Column('id', Integer, primary_key=True),
    Column('title', String),
    Column('date', DateTime),
    Column('body', Text),
    Column('deleted', Boolean)
)


comments = Table('comments', meta,
    Column('id', Integer, primary_key=True),
    Column('title', String),
    Column('date', DateTime),
    Column('comment', Text),
    Column('news_id', Integer, ForeignKey('news.id', ondelete='CASCADE'), index=True)
)


class RecordNotFound(Exception):
    """Requested record in database was not found"""


def row_result_to_dict(row: ResultProxy) -> Dict:
    """Converting ResultProxy object to dict"""
    out_row = []
    for item in row._row:
        if isinstance(item, datetime.datetime):
            out_row.append(item.isoformat())
        else:
            out_row.append(item)
    return dict(zip(row._result_proxy.keys, out_row))


def row_results_to_dict(rows: List) -> List:
    """Converting list of ResultProxy object to list of dict"""
    return [row_result_to_dict(row) for row in rows]


async def pg_context(app):
    conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port']
    )
    app['db'] = engine

    yield

    app['db'].close()
    await app['db'].wait_closed()


async def get_news(conn):
    """Read all news from database"""
    comments_count_subquery = select(
        func.count()) \
        .select_from(comments) \
        .where(comments.c.news_id == news.c.id) \
        .scalar_subquery()
    result = await conn.execute(
        select(news, label('comments_count', comments_count_subquery))
        .where(and_(~news.c.deleted, news.c.date <= datetime.datetime.now()))
        .order_by(news.c.date)
    )
    news_records = await result.fetchall()
    return row_results_to_dict(news_records)


async def get_news_by_id(conn, news_id: int):
    """Read news by id"""
    result = await conn.execute(
        news.select()
        .where(and_(~news.c.deleted, news.c.date <= datetime.datetime.now(), news.c.id == news_id))
        .order_by(news.c.date)
    )
    news_record = await result.first()
    if not news_record:
        msg = "News with id: {} does not exists"
        raise RecordNotFound(msg.format(news_id))

    result = await conn.execute(
        comments.select()
        .where(comments.c.news_id == news_id)
        .order_by(comments.c.date))
    comment_records = await result.fetchall()
    return row_result_to_dict(news_record), row_results_to_dict(comment_records)

