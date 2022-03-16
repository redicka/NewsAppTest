import os
from aiohttp import web
from typing import Optional

from news_app.models import pg_context
from news_app.routes import setup_routes
from news_app.news_api import NewsController
from news_app.settings import load_config

# patch for Windows OS
if os.name == 'nt':
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

conf = load_config()

app = web.Application()


def setup_init(application: Optional[web.Application] = app) -> web.Application:
    # set config
    application['config'] = conf
    # create db connection on startup, shutdown on exit
    application.cleanup_ctx.append(pg_context)

    handler = NewsController()

    setup_routes(application, handler)
    return application


def instance():
    app = setup_init()
    web.run_app(app, host=conf['host'], port=conf['port'])
