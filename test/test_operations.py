"""
Implements tests for omdb_util.py module
"""
import unittest
from unittest import mock

from operations import Operations


class TestOperations(unittest.TestCase):
    def setUp(self):
        self.patch_omdb_util = mock.patch("operations.OMDBUtil")
        self.mock_patch_omdb_util = self.patch_omdb_util.start()

        self.operations = Operations(self.mock_patch_omdb_util)

    def tearDown(self):
        self.patch_omdb_util.stop()

    @mock.patch("operations.Operations.get_movie_model_objects_from_omdb_response")
    def test_get_100_movies_information_from_omdb(
        self, mock_get_movie_model_objects_from_omdb_response
    ):
        mock_get_movie_model_objects_from_omdb_response.return_value = [
            "movie1",
            "movie2",
            "movie3",
            "movie4",
            "movie5",
            "movie6",
            "movie7",
            "movie8",
            "movie9",
            "movie10",
        ]
        result = self.operations.get_100_movies_information_from_omdb()

        # we dont need to check all 100 calls, instead check first and last call
        self.mock_patch_omdb_util().query_omdb.has_calls(
            [
                mock.call(
                    {
                        "s": "marvel",
                        "type": "movie",
                        "page": 1,
                    }
                ),
                mock.call(
                    {
                        "s": "marvel",
                        "type": "movie",
                        "page": 100,
                    }
                ),
            ]
        )
        assert mock_get_movie_model_objects_from_omdb_response.call_count == 10
        assert len(result) == 100

    @mock.patch("operations.Movie")
    def test_get_movie_model_objects_from_omdb_response(self, _):
        resutl = self.operations.get_movie_model_objects_from_omdb_response(
            {
                "Search": [
                    {"title": "movie1", "imdbID": "imdbid1"},
                    {"title": "movie2", "imdbID": "imdbid2"},
                    {"title": "movie3", "imdbID": "imdbid3"},
                ]
            }
        )
        self.mock_patch_omdb_util().query_omdb.has_calls(
            [
                mock.call({"i": "imdbid1"}),
                mock.call({"i": "imdbid2"}),
                mock.call({"i": "imdbid3"}),
            ]
        )
        assert len(resutl) == 3
