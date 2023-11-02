"""Create tables in the database."""


from dotenv import load_dotenv
from loguru import logger
from sqlalchemy import create_engine
from kata_data_foodies.models import metadata
from kata_data_foodies.utils import make_sqlalchemy_db_url

if __name__ == "__main__":
    load_dotenv()

    logger.info("Creating database...")

    db_url = make_sqlalchemy_db_url()
    engine = create_engine(db_url)
    metadata.create_all(bind=engine)

    logger.success("Creation successful!")
