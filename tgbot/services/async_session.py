from typing import Optional

from aiohttp import ClientSession


# Асинхронная сессия для запросов
class AsyncSession:
    def __init__(self) -> None:
        self._session: Optional[ClientSession] = None

    # Вызов сессии
    async def get_session(self) -> ClientSession:
        if self._session is None:
            new_session = ClientSession()
            self._session = new_session

        return self._session

    # Закрытие сессии
    async def close(self) -> None:
        if self._session is None:
            return None

        await self._session.close()
