import os
from database import Base
from sqlalchemy import Integer, VARCHAR, TEXT
from sqlalchemy.orm import Mapped, mapped_column


class Movie(Base):
    """
    Model for table
    """

    __tablename__ = os.environ.get("TABLE_NAME", "omdb_movie_info")

    # Did not take all the fields which OMDB provides, took a few
    # and created the model
    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True)
    imdbid: Mapped[VARCHAR] = mapped_column(VARCHAR(255), unique=True, nullable=False)
    title: Mapped[VARCHAR] = mapped_column(VARCHAR(255))
    year: Mapped[Integer] = mapped_column(Integer, nullable=True)
    genre: Mapped[VARCHAR] = mapped_column(VARCHAR(255), nullable=True)
    released: Mapped[VARCHAR] = mapped_column(VARCHAR(255), nullable=True)
    language: Mapped[VARCHAR] = mapped_column(VARCHAR(255), nullable=True)
    director: Mapped[TEXT] = mapped_column(TEXT, nullable=True)
    writer: Mapped[TEXT] = mapped_column(TEXT, nullable=True)
    actors: Mapped[TEXT] = mapped_column(TEXT, nullable=True)


class Users(Base):
    __tablename__ = "britetest_users"

    username: Mapped[VARCHAR] = mapped_column(
        VARCHAR(255), primary_key=True, unique=True, nullable=False
    )
    password: Mapped[VARCHAR] = mapped_column(VARCHAR(255), nullable=False)
