import logging

from custom_components.atenedgar.edgar import Edgar

logger = logging.getLogger(__name__)


class Aten:
    def __init__(self, edgar: Edgar, name: str):
        self._edgar = edgar
        self.name = name

    async def select_source(self, source: int):
        command = f"sw i0{source}\r\n"
        logger.info(f'Sending command "{command.strip()}"')

        await self._edgar.set(command.encode().hex())
