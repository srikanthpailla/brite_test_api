import os
import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker

# if you want to connect to the database with host and port then
# uncomment below lines and comment out below connect to CloudSQL from CloundRun block

# db_host = os.environ["DB_HOST"]
# db_port = os.environ.get("DB_PORT", 3306)
# db_name = os.environ.get("DB_NAME", "britetest-database")
# db_user = os.environ.get("DB_USER", "britetest-user")
# db_pass = os.environ["DB_PASS"]

# engine = sqlalchemy.create_engine(
#     sqlalchemy.engine.url.URL.create(
#         drivername="mysql+pymysql",
#         username=db_user,
#         password=db_pass,
#         host=db_host,
#         port=db_port,
#         database=db_name,
#     ),
# )


# Connect to CloudSQL from cloudRun app
# https://cloud.google.com/sql/docs/mysql/connect-run
db_user = os.environ.get("DB_USER", "britetest-user")
db_pass = os.environ["DB_PASS"]
db_name = os.environ.get("DB_NAME", "britetest-database")
unix_socket_path = os.environ["INSTANCE_UNIX_SOCKET"]

engine = sqlalchemy.create_engine(
    sqlalchemy.engine.url.URL.create(
        drivername="mysql+pymysql",
        username=db_user,
        password=db_pass,
        database=db_name,
        query={"unix_socket": unix_socket_path},
    ),
)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)
