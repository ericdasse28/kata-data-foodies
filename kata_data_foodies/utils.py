"""Utils."""

import os
import sqlalchemy


def make_sqlalchemy_db_url():
    """Make SQLAlchemy DB URL."""

    db_url = sqlalchemy.URL.create(
        drivername="postgresql",
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        database=os.environ["DB_NAME"],
    )

    return db_url
