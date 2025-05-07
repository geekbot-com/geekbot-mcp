from datetime import datetime

import httpx


class GeekbotClient:
    def __init__(self, api_key: str, version: str = "dev"):
        self.api_key = api_key
        self.version = version
        self.base_url = "https://api.geekbot.com/v1"
        self.headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json",
            "User-Agent": f"geekbot-mcp/{self.version}",
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

    async def post_report(
        self,
        standup_id: int,
        answers: dict[int, dict[str, str]],
    ) -> dict:
        """Post a report"""
        endpoint = f"{self.base_url}/reports/"
        response = await self._client.post(
            endpoint,
            headers=self.headers,
            json={"standup_id": standup_id, "answers": answers},
        )
        response.raise_for_status()
        return response.json()

    async def get_poll_results(
        self, poll_id: int, after: str | None = None, before: str | None = None
    ) -> dict:
        """Fetch poll results

        Args:
            poll_id: int, required, the ID of the poll to fetch results for
            after: str, optional, the date to fetch results after in YYYY-MM-DD format
            before: str, optional, the date to fetch results before in YYYY-MM-DD format
        Returns:
            dict: Properly formatted JSON string of poll results
        """
        endpoint = f"{self.base_url}/polls/{poll_id}/votes/"

        if before and after:
            endpoint = f"{endpoint}?from={after}&to={before}"
        elif before:
            after = "1970-01-01"
            endpoint = f"{endpoint}?from={after}&to={before}"
        elif after:
            before = datetime.now().strftime("%Y-%m-%d")
            endpoint = f"{endpoint}?from={after}&to={before}"

        response = await self._client.get(endpoint, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def close(self):
        self._client.close()
