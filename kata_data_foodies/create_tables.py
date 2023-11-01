"""Create tables in the database."""


from loguru import logger
from sqlalchemy import create_engine
from kata_data_foodies import config
from kata_data_foodies.models import metadata

if __name__ == "__main__":
    logger.info("Creating database...")

    db_url = f"postgresql+psycopg2://{config.DB_USER}:{config.DB_PASSWORD}@\
{config.DB_HOST}:{config.DB_PORT}/recipe_db"
    engine = create_engine(db_url)
    metadata.create_all(bind=engine)

    logger.success("Creation successful!")
