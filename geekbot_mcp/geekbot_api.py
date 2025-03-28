import aiohttp


class GeekbotAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.geekbot.com/v1"
        self._session = None

    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            await self._session.close()

    async def get_standups(self, channel_id: str = None, date: str = None) -> list:
        """Get list of standups"""
        endpoint = f"{self.base_url}/standups/"
        headers = {"Authorization": self.api_key, "Content-Type": "application/json"}

        async with self._session.get(endpoint, headers=headers) as response:
            response.raise_for_status()
            return await response.json()

    async def get_reports(
        self,
        standup_id: int = None,
        user_id: int = None,
        after: int = None,
        before: int = None,
        question_ids: list = None,
        html: bool = None,
    ) -> list:
        """Get list of reports"""
        endpoint = f"{self.base_url}/reports/"
        headers = {"Authorization": self.api_key, "Content-Type": "application/json"}

        params = {"limit": 40}
        if standup_id:
            params["standup_id"] = standup_id
        if user_id:
            params["user_id"] = user_id
        if after:
            params["after"] = after
        if before:
            params["before"] = before
        if question_ids:
            params["question_ids"] = question_ids

        async with self._session.get(
            endpoint, headers=headers, params=params
        ) as response:
            response.raise_for_status()
            return await response.json()
