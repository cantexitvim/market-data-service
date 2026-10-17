import aiohttp


class BaseClient:
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session
