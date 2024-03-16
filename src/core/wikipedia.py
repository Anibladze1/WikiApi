import asyncio

import httpx


class WikipediaClient:
    def __init__(self, base_url="https://en.wikipedia.org/w/api.php"):
        self.base_url = base_url

    async def _make_request(self, parameters):
        """
        Method to Make Requests
        :param parameters: Parameters used to build API call
        :return: Response of API
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url, params=parameters)
            response.raise_for_status()  # Raises an exception for 4XX/5XX errors
            return response.json()

    async def search_topic(self, title: str) -> int:
        """
        Method to Search for a topic and return the page ID.
        :param title: Title of the topic
        :return: Page ID of the topic
        """
        search_params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": title,
        }
        data = await self._make_request(parameters=search_params)
        page_id = data["query"]["search"][0]["pageid"]
        return page_id

    async def retrieve_topic_data(self, topic_title: str) -> dict:
        """
        Method to Retrieve detailed topic data using the Topic title from Wikipedia
        :param topic_title: Title of the topic
        :return: Extracted text from the topic
        """
        page_id = await self.search_topic(title=topic_title)
        topic_data_retrieve_params = {
            "action": "query",
            "format": "json",
            "prop": "extracts",
            "pageids": page_id,
            "explaintext": True,
        }
        data = await self._make_request(parameters=topic_data_retrieve_params)
        topic_details = data["query"]["pages"][str(page_id)]
        data = {
            'text': topic_details['extract'],
            'page_id': page_id
        }
        return data
