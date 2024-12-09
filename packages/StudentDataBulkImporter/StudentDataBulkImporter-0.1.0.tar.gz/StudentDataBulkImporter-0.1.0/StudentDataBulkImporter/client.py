import requests

class APIClient:
    def __init__(self, base_url: str, token: str):
        """
        Initialize the API client.
        :param base_url: Base URL of the FastAPI backend.
        :param token: Authentication token.
        """
        self.base_url = base_url.rstrip("/")
        self.token = token

    def request(self, method: str, endpoint: str, **kwargs):
        """
        Send an HTTP request to the API.
        :param method: HTTP method (e.g., GET, POST).
        :param endpoint: API endpoint.
        :return: JSON response or raises an exception.
        """
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self.token}"
        url = f"{self.base_url}{endpoint}"

        response = requests.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        return response.json()
