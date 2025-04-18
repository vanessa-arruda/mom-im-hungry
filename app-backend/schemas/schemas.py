from pydantic import BaseModel, UUID4, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum
from models.models_recipe import Recipe
from models.models_user import Favorite, RecipeView, UserTags
from models.models_common import Tag


class DifficultyLevel(str, Enum):
    easy = "easy"
    standard = "standard"


# User Schemas
class UserBase(BaseModel):
    email: str
    name: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime
    is_admin: bool = False
    is_active: bool = True
    country_code: Optional[str] = None
    country: Optional[str] = None
    recipes: List["Recipe"] = []
    tags: List[Tag] = []
    favorites: List[Favorite] = []
    recipe_views: List[RecipeView] = []
    user_tags: List[UserTags] = []

    class Config:
        orm_mode = True


# Ingredient Schemas
class IngredientBase(BaseModel):
    name: str
    ingredient_type_id: Optional[int]
    color: Optional[str]
    kcal_per_100: float
    measurement_preference: str
    is_liquid: bool = False
    is_spice: bool = False


class IngredientCreate(IngredientBase):
    pass


class Ingredient(IngredientBase):
    id: int

    class Config:
        orm_mode = True


# Measurement Unit Schemas
class MeasurementUnitBase(BaseModel):
    name: str
    type: str
    conversion_to_grams: Optional[float]
    conversion_to_ml: Optional[float]


class MeasurementUnit(MeasurementUnitBase):
    id: int

    class Config:
        orm_mode = True


# Recipe Ingredient Schema (nested inside Recipe)
class RecipeIngredientBase(BaseModel):
    ingredient_id: int
    quantity: float
    unit_id: int
    notes: Optional[str]


class RecipeIngredientCreate(RecipeIngredientBase):
    pass


class RecipeIngredient(RecipeIngredientBase):
    id: int
    ingredient: Ingredient
    unit: MeasurementUnit

    class Config:
        orm_mode = True


# Recipe Schemas
class RecipeBase(BaseModel):
    title: str
    description: Optional[str]
    instructions: str
    country_code: Optional[str]
    meal_type_id: Optional[int]
    difficulty: DifficultyLevel
    season_id: Optional[int]
    cooking_duration_minutes: Optional[int]
    calories_total: Optional[int]
    is_public: bool = True


class RecipeCreate(RecipeBase):
    ingredients: List[RecipeIngredientCreate]


class Recipe(RecipeBase):
    id: UUID4
    created_by: UUID4
    created_at: datetime
    ingredients: List[RecipeIngredient]

    class Config:
        orm_mode = True
