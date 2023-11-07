import os
import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker


db_host = os.environ["DB_HOST"]
db_user = os.environ.get("DB_USER", "britetest-user")
db_pass = os.environ["DB_PASS"]
db_name = os.environ.get("DB_NAME", "britetest-database")
db_port = os.environ.get("DB_PORT", 3306)

engine = sqlalchemy.create_engine(
    sqlalchemy.engine.url.URL.create(
        drivername="mysql+pymysql",
        username=db_user,
        password=db_pass,
        host=db_host,
        port=db_port,
        database=db_name,
    ),
)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)
