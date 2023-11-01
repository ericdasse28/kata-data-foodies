"""Models."""

import sqlalchemy

metadata = sqlalchemy.MetaData()

recipes = sqlalchemy.Table(
    "recipes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, autoincrement=True),
    sqlalchemy.Column("recipe_name", sqlalchemy.String),
    sqlalchemy.Column("is_vegetarian", sqlalchemy.Boolean),
    sqlalchemy.Column("is_vegan", sqlalchemy.Boolean),
    sqlalchemy.Column("is_gluten_free", sqlalchemy.Boolean),
    sqlalchemy.Column("instructions", sqlalchemy.Text),
    sqlalchemy.Column("ingredients", sqlalchemy.ARRAY(sqlalchemy.String)),
)
