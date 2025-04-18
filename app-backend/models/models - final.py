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
    Table,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

from datetime import datetime
from database import Base
import enum


class DifficultyEnum(str, enum.Enum):
    easy = "easy"
    standard = "standard"
    advanced = "advanced"


class MeasurementPreferenceEnum(str, enum.Enum):
    grams = "grams"
    ml = "ml"
    unit = "unit"


class MeasurementTypeEnum(str, enum.Enum):
    weight = "weight"
    volume = "volume"
    count = "count"


class Country(Base):
    __tablename__ = "countries"
    code = Column(String, primary_key=True)
    name = Column(String)


class MealType(Base):
    __tablename__ = "meal_types"
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Season(Base):
    __tablename__ = "seasons"
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Favorite(Base):
    __tablename__ = "favorites"
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    recipe_id = Column(UUID(as_uuid=True), ForeignKey("recipes.id"))
    liked = Column(Boolean)
    made_it = Column(Boolean)
    rating = Column(Integer)


class RecipeView(Base):
    __tablename__ = "recipe_views"
    id = Column(Integer, primary_key=True)
    recipe_id = Column(UUID(as_uuid=True), ForeignKey("recipes.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    viewed_at = Column(DateTime, default=datetime.utcnow)


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class RecipeTag(Base):
    __tablename__ = "recipe_tags"
    recipe_id = Column(UUID(as_uuid=True), ForeignKey("recipes.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)

    recipe = relationship("Recipe", back_populates="tags")


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    recipes = relationship("Recipe", back_populates="creator")


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
    created_at = Column(DateTime, default=datetime.utcnow)
    is_public = Column(Boolean, default=True)

    creator = relationship("User", back_populates="recipes")
    ingredients = relationship("RecipeIngredient", back_populates="recipe")
    tags = relationship("RecipeTag", back_populates="recipe")


class IngredientType(Base):
    __tablename__ = "ingredient_types"
    id = Column(Integer, primary_key=True)
    name = Column(String)


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


class MeasurementUnit(Base):
    __tablename__ = "measurement_units"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(Enum(MeasurementTypeEnum))
    conversion_to_grams = Column(Float, nullable=True)
    conversion_to_ml = Column(Float, nullable=True)


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"
    id = Column(Integer, primary_key=True)
    recipe_id = Column(UUID(as_uuid=True), ForeignKey("recipes.id"))
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"))
    quantity = Column(Float)
    unit_id = Column(Integer, ForeignKey("measurement_units.id"))
    notes = Column(String)

    recipe = relationship("Recipe", back_populates="ingredients")
