
def setup_routes(app, handler):
    router = app.router
    h = handler
    router.add_get('/', h.get_news, name='news')
    router.add_get('/news/{id}', h.get_news_by_id, name='news_by_id')
