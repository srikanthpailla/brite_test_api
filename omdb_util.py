import os
import requests
from starlette.config import Config
from requests.adapters import HTTPAdapter, Retry
from fastapi import HTTPException


class OMDBUtil:
    def __init__(self):
        self.omdb_url = os.environ.get("OMDB_URL", "https://www.omdbapi.com/")
        self.api_key = os.environ["OMDB_API_KEY"]
        self.request_session = self._create_request_session()

    def _create_request_session(self):
        request_session = requests.Session()
        retries = Retry(
            total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504]
        )
        request_session.mount("https://", HTTPAdapter(max_retries=retries))
        return request_session

    def query_omdb(self, params):
        headers = {"Accept": "application/json"}
        params.update({"apikey": self.api_key})
        response = self.request_session.get(
            self.omdb_url, headers=headers, params=params
        )
        response.raise_for_status()
        if response.json().get("Response") == "False":
            raise HTTPException(404, detail="Movie Not Found in OMDB.")
        return response.json()
