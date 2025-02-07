import logging

import aiohttp

logger = logging.getLogger(__name__)


class Edgar:
    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port
        self._timeout = aiohttp.ClientTimeout(total=5)

    def get_base_url(self) -> str:
        return f"http://{self._host}:{self._port}"

    async def is_reachable(self) -> bool:
        async with aiohttp.ClientSession(timeout=self._timeout) as session:
            try:
                url = self.get_base_url()
                logger.debug(f"Requesting URL {url}")

                async with session.get(url) as response:
                    return response.status == 200
            except (TimeoutError, aiohttp.ClientError) as e:
                logger.error(e)
                return False

    async def set(self, hex: str) -> int:
        async with aiohttp.ClientSession(timeout=self._timeout) as session:
            url = f"{self.get_base_url()}/set.xml?hex={hex}"
            logger.debug(f"Requesting URL {url}")

            async with session.get(url) as response:
                return response.status
