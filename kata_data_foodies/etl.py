"""Spoonacular ETL"""

from dotenv import load_dotenv
import requests
from sqlalchemy import create_engine, text
from kata_data_foodies import config
from typing import List, Dict


def extract():
    """Extract."""

    response = requests.get(
        "https://api.spoonacular.com/recipes/random?number=200",
        params={"apiKey": config.SPOONACULAR_API_KEY},
    )
    recipes = response.json()["recipes"]

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
            recipe_insert_stmt = text(
                """
                INSERT INTO recipes
                (id, recipe_name, is_vegetarian, is_vegan, is_gluten_free,
                instructions, ingredients)
                VALUES (:id, :recipe_name, :is_vegetarian, :is_vegan,
                :is_gluten_free, :instructions, array[:ingredients])
"""
            )
            connection.execute(
                recipe_insert_stmt,
                recipe_name=transformed_recipe["recipe_name"],
                is_vegetarian=transformed_recipe["is_vegetarian"],
                is_vegan=transformed_recipe["is_vegan"],
                is_gluten_free=transformed_recipe["is_gluten_free"],
                instructions=transformed_recipe["instructions"],
                ingredients=transformed_recipe["ingredients"],
            )


def main():
    """Main."""

    load_dotenv()

    recipes = extract()
    transformed_recipes = transform(recipes)
    load(transformed_recipes)


if __name__ == "__main__":
    main()
