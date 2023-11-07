import logging
import models
import serializers

from database import Base, engine

logging.basicConfig(
    format="%(asctime)s [ %(module)s ] [ %(funcName)s ] %(levelname)s -- %(message)s"
)
log = logging.getLogger(__name__)
log.setLevel(level=logging.DEBUG)


Base.metadata.create_all(engine)
