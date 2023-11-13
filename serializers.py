from pydantic import BaseModel


class Movie(BaseModel):
    id: int
    imdbid: str
    title: str
    year: int
    genre: str
    released: str
    language: str
    director: str
    writer: str
    actors: str

    class Config:
        orm_mode = True


class Users(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True
