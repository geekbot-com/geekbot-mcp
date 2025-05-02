import httpx


class GeekbotClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.geekbot.com/v1"
        self.headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json",
        }
        self._client = httpx.AsyncClient(headers=self.headers, timeout=40)

    async def get_standups(
        self,
    ) -> list:
        """Get list of standups"""
        endpoint = f"{self.base_url}/standups/"
        response = await self._client.get(endpoint, headers=self.headers)
        response.raise_for_status()
        return response.json()

    async def get_polls(self) -> list:
        """Get list of polls"""
        endpoint = f"{self.base_url}/polls/"
        response = await self._client.get(endpoint, headers=self.headers)
        response.raise_for_status()
        return response.json()

    async def get_reports(
        self,
        standup_id: int | None = None,
        user_id: int | None = None,
        after: int | None = None,
        before: int | None = None,
        question_ids: list | None = None,
        limit: int = 50,
    ) -> list:
        """Get list of reports"""
        endpoint = f"{self.base_url}/reports/"

        params = {"limit": limit}
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

        response = await self._client.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    async def get_poll_results(
        self, poll_id: int, after: int | None = None, before: int | None = None
    ) -> dict:
        """Fetch poll results"""
        endpoint = f"{self.base_url}/polls/{poll_id}/votes/"
        params = {}
        if after:
            params["after"] = after
        if before:
            params["before"] = before

        response = await self._client.get(endpoint, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def close(self):
        self._client.close()
