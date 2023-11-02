"""Spoonacular ETL"""

import os
from dotenv import load_dotenv
from loguru import logger
import requests
from sqlalchemy import create_engine, insert
import sqlalchemy
from typing import List, Dict
from kata_data_foodies.models import recipes


def extract():
    """Extract."""

    spoonacular_api_key = os.environ["SPOONACULAR_API_KEY"]

    response = requests.get(
        "https://api.spoonacular.com/recipes/random?number=200",
        params={"apiKey": spoonacular_api_key},
    )
    if response.status_code == 200:
        recipes = response.json()["recipes"]
    else:
        raise Exception("The request failed!")

    return recipes


def transform(recipes: List[Dict]) -> List[Dict]:
    """Transform."""

    transformed_recipes = []

    for recipe in recipes:
        transformed_recipes.append(
            {
                "recipe_name": recipe["title"],
                "is_vegetarian": recipe["vegetarian"],
                "is_vegan": recipe["vegan"],
                "is_gluten_free": recipe["glutenFree"],
                "instructions": recipe["instructions"],
                "ingredients": [
                    ingredient["name"]
                    for ingredient in recipe["extendedIngredients"]  # noqa
                ],
            }
        )

    return transformed_recipes


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


def load(transformed_recipes: List[Dict]):
    """Load."""

    db_url = make_sqlalchemy_db_url()
    engine = create_engine(
        db_url,
        execution_options={"isolation_level": "AUTOCOMMIT"},
    )

    with engine.connect() as connection:
        for transformed_recipe in transformed_recipes:
            recipe_insert_stmt = insert(recipes).values(
                recipe_name=transformed_recipe["recipe_name"],
                is_vegetarian=transformed_recipe["is_vegetarian"],
                is_vegan=transformed_recipe["is_vegan"],
                is_gluten_free=transformed_recipe["is_gluten_free"],
                instructions=transformed_recipe["instructions"],
                ingredients=transformed_recipe["ingredients"],
            )
            connection.execute(recipe_insert_stmt)


def main():
    """Main."""

    logger.info("Acquiring data from Spoonacular API")
    recipes = extract()
    logger.info("Transformation...")
    transformed_recipes = transform(recipes)
    logger.info("Loading")
    load(transformed_recipes)

    logger.success("ETL successful!")


if __name__ == "__main__":
    load_dotenv()

    main()
