"""
Implements tests for omdb_util.py module
"""
import unittest
import os
from unittest import mock

from fastapi import HTTPException
from omdb_util import OMDBUtil


class TestOMDBUtil(unittest.TestCase):
    def setUp(self):
        os.environ["OMDB_API_KEY"] = "12345678"

    def tearDown(self):
        del os.environ["OMDB_API_KEY"]

    @mock.patch("omdb_util.OMDBUtil._create_request_session")
    def test_query_omdb(self, mock_create_request_session):
        response_mock = mock.MagicMock()

        requests_mock = mock.MagicMock()
        requests_mock.get.return_value = response_mock

        mocked_search_data = {
            "Search": [
                {
                    "Title": "Captain Marvel",
                },
                {
                    "Title": "Ms. Marvel",
                },
            ]
        }
        response_mock.json.return_value = mocked_search_data
        mock_create_request_session.return_value = requests_mock

        params = {
            "s": "marvel",
            "type": "movie",
            "page": 1,
        }
        result = OMDBUtil().query_omdb(params)

        requests_mock.get.assert_called_with(
            "https://www.omdbapi.com/",
            headers={"Accept": "application/json"},
            params={"s": "marvel", "type": "movie", "page": 1, "apikey": "12345678"},
        )
        self.assertDictEqual(result, mocked_search_data)

    @mock.patch("omdb_util.OMDBUtil._create_request_session")
    def test_query_omdb_failure(self, mock_create_request_session):
        response_mock = mock.MagicMock()

        requests_mock = mock.MagicMock()
        requests_mock.get.return_value = response_mock

        mocked_search_data = {"Response": "False", "Error": "Item not found"}
        response_mock.json.return_value = mocked_search_data
        mock_create_request_session.return_value = requests_mock

        params = {
            "i": "tt4154664",
        }
        with self.assertRaises(HTTPException):
            OMDBUtil().query_omdb(params)

        requests_mock.get.assert_called_with(
            "https://www.omdbapi.com/",
            headers={"Accept": "application/json"},
            params={"i": "tt4154664", "apikey": "12345678"},
        )
