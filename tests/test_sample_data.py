from aiohttp.test_utils import AioHTTPTestCase
from aiohttp import web
from news_app.main import setup_init


class NewsAppTestAPICase(AioHTTPTestCase):

    async def get_application(self):
        """
        Override the get_app method to return your application.
        """
        app = web.Application()
        return setup_init(app)

    async def test_get_all_news(self):
        async with self.client.request("GET", "/") as resp:
            # check status
            self.assertEqual(resp.status, 200)
            json_data = await resp.json()
            # check news rows count
            self.assertEqual(len(json_data['news']), 1)
            # check equal news length and news counts
            self.assertEqual(len(json_data['news']), json_data['news_count'])

    async def test_get_news_by_id(self):
        async with self.client.request("GET", "/news/1") as resp:
            # check status
            self.assertEqual(resp.status, 200)
            json_data = await resp.json()
            # check comments rows count
            self.assertEqual(len(json_data['comments']), 1)
            # check equal news length and news counts
            self.assertEqual(len(json_data['comments']), json_data['comments_count'])

    async def test_get_news_by_fake_id(self):
        async with self.client.request("GET", "/news/2") as resp:
            # check status
            self.assertEqual(resp.status, 404)



