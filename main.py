"""
Main module
"""
import auth_handler
import logging
import models
import os
import serializers

from contextlib import asynccontextmanager
from datetime import timedelta
from database import Base, SessionLocal, engine
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from omdb_util import OMDBUtil
from operations import Operations
from sqlalchemy.orm import Session


logging.basicConfig(
    format="%(asctime)s [ %(module)s ] [ %(funcName)s ] %(levelname)s -- %(message)s"
)
log = logging.getLogger(__name__)
log.setLevel(level=logging.DEBUG)

if not os.environ.get("fastApiUnittest"):
    Base.metadata.create_all(engine)

omdb_util = OMDBUtil()
operations = Operations(omdb_util)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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


@app.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = auth_handler.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth_handler.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_handler.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


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
async def remove_movie(
    id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """
    Route to delete movie by param id
    """
    if not auth_handler.get_current_user(db, token):
        raise HTTPException(401, detail="Authentication failed")
    result = db.query(models.Movie).filter_by(id=id).delete()
    db.commit()
    if not result:
        raise HTTPException(404, detail=f"Movie with id: {id} not found")
    return {"1 row": "removed"}


@app.post("/singup")
async def signUp(new_user: serializers.Users, db: Session = Depends(get_db)):
    new_user = models.Users(
        username=new_user.username,
        password=auth_handler.get_password_hash(new_user.password),
    )
    db.add(new_user)
    db.commit()
    return {"signup": "Successful"}
