import logging
from omdb_util import OMDBUtil
from models import Movie

logging.basicConfig(
    format="%(asctime)s [ %(module)s ] [ %(funcName)s ] %(levelname)s -- %(message)s"
)
log = logging.getLogger(__name__)
log.setLevel(level=logging.DEBUG)


class OperationsException(Exception):
    """Operations exception"""


class Operations:
    def __init__(self, omdb_util: OMDBUtil):
        self.omdb_util = omdb_util

    def get_100_movies_information_from_omdb(self):
        """
        Get 100 movies information and convert them
        to list of Movie Model objects
        """
        movie_data = []
        for page in range(1, 11):
            params = {
                "s": "marvel",
                "type": "movie",
                "page": page,
            }
            response_json = self.omdb_util.query_omdb(params)
            log.info(f"Adding page: {page}")
            movie_data.extend(
                self.get_movie_model_objects_from_omdb_response(response_json)
            )
        return movie_data

    def get_movie_model_objects_from_omdb_response(self, search_response_from_omdb):
        """
        Format list of model objects from omdb search
        response
        """
        values = []
        for movie_info in search_response_from_omdb["Search"]:
            imdb_id = movie_info["imdbID"]
            params = {"i": imdb_id}
            response = self.omdb_util.query_omdb(params)
            values.append(
                Movie(
                    imdbid=response["imdbID"],
                    title=response["Title"],
                    year=response["Year"],
                    genre=response["Genre"],
                    released=response["Released"],
                    language=response["Language"],
                    director=response["Director"],
                    writer=response["Writer"],
                    actors=response["Actors"],
                )
            )
        return values

    def get_movie_info(self, title):
        """
        Get movie info for the provided
        title from OMDB and return movie model
        object
        """
        params = {"t": title}
        response = self.omdb_util.query_omdb(params)
        return Movie(
            imdbid=response["imdbID"],
            title=response["Title"],
            year=response["Year"],
            genre=response["Genre"],
            released=response["Released"],
            language=response["Language"],
            director=response["Director"],
            writer=response["Writer"],
            actors=response["Actors"],
        )
