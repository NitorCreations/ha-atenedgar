import logging
import xml.dom.minidom

from dataclasses import dataclass

import aiohttp

logger = logging.getLogger(__name__)


@dataclass
class EdgarSettings:
    ip: str
    type: str
    mac: str
    fw: str


def parse_settings_xml(settings_xml: str):
    dom = xml.dom.minidom.parseString(settings_xml)
    sets = dom.getElementsByTagName("set")

    ip = ""
    type = ""
    mac = ""
    fw = ""

    for set in sets:
        box = set.getAttribute("box")

        match box:
            case "1":
                ip = set.getAttribute("ip")
            case "12":
                type = set.getAttribute("type")
                mac = set.getAttribute("mac")
                fw = set.getAttribute("fw")

    return EdgarSettings(ip, type, mac, fw)


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

    async def get_settings(self) -> EdgarSettings | None:
        async with aiohttp.ClientSession(timeout=self._timeout) as session:
            try:
                url = f"{self.get_base_url()}/settings.xml"
                logger.debug(f"Requesting URL {url}")

                async with session.get(url) as response:
                    settings_xml = await response.text(encoding="iso-8859-2")

                    return parse_settings_xml(settings_xml)
            except (TimeoutError, aiohttp.ClientError) as e:
                logger.error(e)
