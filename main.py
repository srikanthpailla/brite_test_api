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
    db = await get_db().__anext__()
    if not db.query(models.Movie).first():
        values = operations.populate_db_with_initial_data()
        db.add_all(values)
        db.commit()
    else:
        log.info("Data exists, skiping populating of movie data from OMDB")
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def docs_redirect():
    return RedirectResponse(url="/docs")


@app.get("/list", response_model=Page[serializers.Movie])
async def list_movie(db: Session = Depends(get_db), page: int = 1, perpage: int = 10):
    params = Params(size=perpage, page=page)
    return paginate(db, db.query(models.Movie).order_by(models.Movie.title), params)


@app.get("/single")
async def single_movie(db: Session = Depends(get_db), title: str = None):
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
