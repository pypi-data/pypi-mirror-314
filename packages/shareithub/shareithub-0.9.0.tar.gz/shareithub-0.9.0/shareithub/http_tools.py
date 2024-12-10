import requests
from fake_useragent import UserAgent
import aiohttp

class HTTPTools:
    @staticmethod
    def get(url):
        ua = UserAgent()
        headers = {"User-Agent": ua.random}
        response = requests.get(url, headers=headers)
        return response.text

    @staticmethod
    async def async_get(url):
        ua = UserAgent()
        headers = {"User-Agent": ua.random}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as response:
                return await response.text()
