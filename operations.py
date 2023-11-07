import logging
import calendar
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

    def populate_db_with_initial_data(self):
        movie_data = []
        for page in range(1, 11):
            params = {
                "s": "marvel",
                "type": "movie",
                "page": page,
            }
            response_json = self.omdb_util.query_omdb(params)
            log.info(f"Adding page: {page}")
            movie_data.extend(self.get_movie_info_and_add_to_db(response_json))
        return movie_data

    def get_movie_info_and_add_to_db(self, search_response_from_omdb):
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

    def add_movie(self, title):
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
