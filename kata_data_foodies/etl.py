"""Spoonacular ETL"""

from dotenv import load_dotenv
from loguru import logger
import requests
from sqlalchemy import create_engine, insert
from kata_data_foodies import config
from typing import List, Dict
from kata_data_foodies.models import recipes


def extract():
    """Extract."""

    response = requests.get(
        "https://api.spoonacular.com/recipes/random?number=200",
        params={"apiKey": config.SPOONACULAR_API_KEY},
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


def load(transformed_recipes: List[Dict]):
    """Load."""

    db_url = f"postgresql+psycopg2://{config.DB_USER}:{config.DB_PASSWORD}@\
{config.DB_HOST}:{config.DB_PORT}/recipe_db"
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


if __name__ == "__main__":
    load_dotenv()

    main()
