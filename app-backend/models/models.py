import uuid
from sqlalchemy import (
    Column,
    String,
    Text,
    Enum,
    Boolean,
    Integer,
    ForeignKey,
    DateTime,
    Numeric,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum


# Difficulty levels enum
class DifficultyLevel(enum.Enum):
    easy = "easy"
    standard = "standard"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    recipes = relationship("Recipe", back_populates="creator")


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text)
    instructions = Column(Text)  # or use JSON for step-by-step if needed
    country_code = Column(String, ForeignKey("countries.code"), nullable=True)
    meal_type_id = Column(Integer, ForeignKey("meal_types.id"), nullable=True)
    difficulty = Column(Enum(DifficultyLevel), nullable=False)
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=True)
    cooking_duration_minutes = Column(Integer)
    calories_total = Column(Integer)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_public = Column(Boolean, default=True)

    creator = relationship("User", back_populates="recipes")
    ingredients = relationship("RecipeIngredient", back_populates="recipe")


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    ingredient_type_id = Column(Integer, ForeignKey("ingredient_types.id"))
    color = Column(String, nullable=True)
    kcal_per_100 = Column(Numeric)
    measurement_preference = Column(
        Enum("grams", "ml", "unit", name="measurement_preference")
    )
    is_liquid = Column(Boolean, default=False)
    is_spice = Column(Boolean, default=False)

    recipe_ingredients = relationship("RecipeIngredient", back_populates="ingredient")


class MeasurementUnit(Base):
    __tablename__ = "measurement_units"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # e.g. grams, ml, cup
    type = Column(Enum("weight", "volume", "count", name="unit_type"))
    conversion_to_grams = Column(Numeric, nullable=True)
    conversion_to_ml = Column(Numeric, nullable=True)


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(UUID(as_uuid=True), ForeignKey("recipes.id"), nullable=False)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)
    quantity = Column(Numeric, nullable=False)
    unit_id = Column(Integer, ForeignKey("measurement_units.id"), nullable=False)
    notes = Column(String, nullable=True)

    recipe = relationship("Recipe", back_populates="ingredients")
    ingredient = relationship("Ingredient", back_populates="recipe_ingredients")
    unit = relationship("MeasurementUnit")
