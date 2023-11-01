"""Models."""

from sqlalchemy import Table, MetaData, Column, Integer, String, Boolean, ARRAY

metadata = MetaData()

recipes = Table(
    "recipes",
    metadata,
    Column("id", Integer, autoincrement=True),
    Column("recipe_name", String),
    Column("is_vegetarian", Boolean),
    Column("is_vegan", Boolean),
    Column("is_gluten_free", Boolean),
    Column("instructions", String),
    Column("ingredients", ARRAY(String)),
)
