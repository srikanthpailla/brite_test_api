"""
Main module
"""
import logging
import models
import serializers

from contextlib import asynccontextmanager
from database import Base, SessionLocal, engine
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from omdb_util import OMDBUtil
from operations import Operations
from sqlalchemy.orm import Session

logging.basicConfig(
    format="%(asctime)s [ %(module)s ] [ %(funcName)s ] %(levelname)s -- %(message)s"
)
log = logging.getLogger(__name__)
log.setLevel(level=logging.DEBUG)


Base.metadata.create_all(engine)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


omdb_util = OMDBUtil()
operations = Operations(omdb_util)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # get db object from get_db generator
    db = await get_db().__anext__()

    # check if table is empty, populate db with data only if table is empty
    if not db.query(models.Movie).first():
        values = operations.get_100_movies_information_from_omdb()
        db.add_all(values)
        db.commit()
    else:
        log.info("Don't need to populate db with data as data aleady exists")
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def docs_redirect():
    return RedirectResponse(url="/docs")


@app.get("/list", response_model=Page[serializers.Movie])
async def list_movie(db: Session = Depends(get_db), page: int = 1, perpage: int = 10):
    """
    Route to lists movies with pagination
    Default page size is 10
    """
    params = Params(size=perpage, page=page)
    return paginate(db, db.query(models.Movie).order_by(models.Movie.title), params)


@app.get("/single")
async def single_movie(db: Session = Depends(get_db), title: str = None):
    """
    Route to get single movie
    param title to get movie by title, this param is optional
    by default it will return first row
    """
    if title:
        single_movie = (
            db.query(models.Movie).filter(models.Movie.title == title).limit(1).all()
        )
        single_movie = single_movie[0] if single_movie else None
    else:
        single_movie = db.query(models.Movie).first()
    if not single_movie:
        raise HTTPException(404, detail="Movie not found")
    return single_movie


@app.post("/add", response_model=serializers.Movie)
async def add_movie(title: str, db: Session = Depends(get_db)):
    """
    Route to add movie by param title
    Gets movie information from OMDB based on title param and add it to db
    """
    if db.query(models.Movie).filter_by(title=title).first() is not None:
        raise HTTPException(409, detail="Movie already exists in database")
    movie_to_be_added = operations.get_movie_info(title)
    db.add(movie_to_be_added)
    db.commit()
    return movie_to_be_added


@app.delete("/remove")
async def remove_movie(id: int, db: Session = Depends(get_db)):
    """
    Route to delete movie by param id
    """
    result = db.query(models.Movie).filter_by(id=id).delete()
    db.commit()
    if not result:
        raise HTTPException(404, detail=f"Movie with id: {id} not found")
    return {"1 row": "removed"}
