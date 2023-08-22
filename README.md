# Kata Data Foodies
Kata to practice data engineering skills. And because food is always worth mixing business with pleasure, here goes a kata around it!

## Statement
You work for a company called _Food Magic_ as a **data engineer**. A team of data scientists is interested in analyzing different recipes (why you ask? I don't know but let the fellows cook). To achieve their purpose, they want a database of 200 recipes and don't particularly care about _what_ recipes. However, they do care about the information given about those recipes. Specifically, they want to know the following information about the recipes:

- `recipe_name`: name of the recipe
- `is_vegetarian`: true if the recipe is vegeterian, false otherwise
- `is_vegan`: you get it
- `is_gluten_free`: true if the recipe is gluten free, false otherwise
- `instructions`: instructions to perform that recipe
- The ingredients

And that's where you come in! Your job is to build a [PostgreSQL database](https://www.postgresql.org/download/) containing those 200 recipes and the related information.

## Data source : [Spoonacular API](https://spoonacular.com/food-api)
After discussing with the team, you agreed to use [Spoonacular API](https://spoonacular.com/food-api) to obtain those recipes. Specifically, you will use the [random recipes endpoint](https://spoonacular.com/food-api/docs#Get-Random-Recipes) of that API:

```
GET https://api.spoonacular.com/recipes/random
```
To use the Spoonacular API, you will have to create an account first (don't worry it's free) which will in turn give you access to an API key.

Note: I advise you to explore the data returned by that endpoint to get ahold of where are the information you are looking for. You could use [Postman](https://www.postman.com/downloads/) for example.

## Creating the ETL
To feed the recipe database you want to create, you will write a script in the language of your choice (ex. Python) that will be used as an ETL.

Happy coding!
