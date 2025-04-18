import uuid
from sqlalchemy import (
    Column,
    String,
    Text,
    Boolean,
    Enum,
    ForeignKey,
    Integer,
    DateTime,
    Float,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

from datetime import datetime
from database import Base

from models.models_common import (
    DifficultyEnum,
    MeasurementPreferenceEnum,
    MeasurementTypeEnum,
    SeasonEnum,
)


class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    description = Column(Text)
    instructions = Column(JSONB)
    country_code = Column(String, ForeignKey("countries.code"))
    meal_type_id = Column(Integer, ForeignKey("meal_types.id"))
    difficulty = Column(Enum(DifficultyEnum))
    season_id = Column(Integer, ForeignKey("seasons.id"))
    cooking_duration_minutes = Column(Integer)
    calories_total = Column(Integer)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.now)
    is_public = Column(Boolean, default=True)
    creator = relationship("User", back_populates="recipes")
    ingredients = relationship("RecipeIngredient", back_populates="recipe")
    tags = relationship("RecipeTag", back_populates="recipes")


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"
    id = Column(Integer, primary_key=True)
    recipe_id = Column(UUID(as_uuid=True), ForeignKey("recipes.id"))
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"))
    quantity = Column(Float)
    unit_id = Column(Integer, ForeignKey("measurement_units.id"))
    notes = Column(String)

    recipe = relationship("Recipe", back_populates="ingredients")


class Ingredient(Base):
    __tablename__ = "ingredients"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    ingredient_type_id = Column(Integer, ForeignKey("ingredient_types.id"))
    color = Column(String)
    kcal_per_100 = Column(Float)
    measurement_preference = Column(Enum(MeasurementPreferenceEnum))
    is_liquid = Column(Boolean)
    is_spice = Column(Boolean)


class IngredientType(Base):
    __tablename__ = "ingredient_types"
    id = Column(Integer, primary_key=True)
    name = Column(String)


class MealType(Base):
    __tablename__ = "meal_types"
    id = Column(Integer, primary_key=True)
    name = Column(String)


class MeasurementUnit(Base):
    __tablename__ = "measurement_units"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(Enum(MeasurementTypeEnum))
    conversion_to_grams = Column(Float, nullable=True)
    conversion_to_ml = Column(Float, nullable=True)


class Season(Base):
    __tablename__ = "seasons"
    id = Column(Integer, primary_key=True)
    name = Column(Enum(SeasonEnum))


class RecipeTag(Base):
    __tablename__ = "recipe_tags"
    recipe_id = Column(UUID(as_uuid=True), ForeignKey("recipes.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)
    recipe = relationship("Recipe", back_populates="tags")
    tag = relationship("Tag", back_populates="recipes")
