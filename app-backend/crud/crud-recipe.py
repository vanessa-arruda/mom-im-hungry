from sqlalchemy.orm import Session
from sqlalchemy import func
from uuid import uuid4
from models.models import Recipe, RecipeIngredient, Ingredient, MeasurementUnit
from schemas.schemas import RecipeCreate, RecipeIngredientCreate


# Create Recipe
def create_recipe(db: Session, recipe: RecipeCreate, user_id: uuid4):
    db_recipe = Recipe(
        title=recipe.title,
        description=recipe.description,
        instructions=recipe.instructions,
        country_code=recipe.country_code,
        meal_type_id=recipe.meal_type_id,
        difficulty=recipe.difficulty,
        season_id=recipe.season_id,
        cooking_duration_minutes=recipe.cooking_duration_minutes,
        calories_total=recipe.calories_total,
        created_by=user_id,
        is_public=recipe.is_public,
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)

    # Now, add ingredients to the recipe (via RecipeIngredient)
    for ingredient in recipe.ingredients:
        db_recipe_ingredient = RecipeIngredient(
            recipe_id=db_recipe.id,
            ingredient_id=ingredient.ingredient_id,
            quantity=ingredient.quantity,
            unit_id=ingredient.unit_id,
            notes=ingredient.notes,
        )
        db.add(db_recipe_ingredient)

    db.commit()
    return db_recipe


# Get Recipe by ID
def get_recipe_by_id(db: Session, recipe_id: uuid4):
    return db.query(Recipe).filter(Recipe.id == recipe_id).first()


# Get all Recipes (optional: can add pagination later)
def get_recipes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Recipe).offset(skip).limit(limit).all()


# Get Recipes by Ingredient (example search by ingredient name)
def get_recipes_by_ingredient(
    db: Session, ingredient_name: str, skip: int = 0, limit: int = 100
):
    return (
        db.query(Recipe)
        .join(RecipeIngredient)
        .join(Ingredient)
        .filter(Ingredient.name == ingredient_name)
        .offset(skip)
        .limit(limit)
        .all()
    )


# Get all Ingredients
def get_ingredients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Ingredient).offset(skip).limit(limit).all()


# Get Measurement Units
def get_measurement_units(db: Session):
    return db.query(MeasurementUnit).all()
