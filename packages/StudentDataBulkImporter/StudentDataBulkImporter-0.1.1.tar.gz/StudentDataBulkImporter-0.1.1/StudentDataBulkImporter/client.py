import requests
import pymysql
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

class DatabaseClient:
    def __init__(self, db_url: str):
        """
        Initialize the database client.
        :param db_url: Database connection URL.
        """
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def execute_query(self, query: str, params=None):
        """
        Execute a SQL query and return the result.
        :param query: SQL query as a string.
        :param params: Parameters for the query.
        :return: Query result.
        """
        with self.SessionLocal() as session:
            result = session.execute(text(query), params)
            return result.fetchall()

    def close(self):
        """Dispose of the engine."""
        self.engine.dispose()
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
