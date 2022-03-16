from aiohttp import web
from . import models


class NewsController:

    async def get_news(self, request):
        async with request.app['db'].acquire() as conn:
            try:
                news = await models.get_news(conn)
            except models.RecordNotFound as e:
                raise web.HTTPNotFound(text=str(e))
            return web.json_response({
                'news': news,
                'news_count': len(news)
            })

    async def get_news_by_id(self, request):
        async with request.app['db'].acquire() as conn:
            news_id = request.match_info['id']
            try:
                news_record, comments = await models.get_news_by_id(conn, news_id)
                news_record.update({
                    'comments': comments,
                    'comments_count': len(comments)
                })
            except models.RecordNotFound as e:
                raise web.HTTPNotFound(text=str(e))
            return web.json_response(news_record)
