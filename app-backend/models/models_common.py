from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from database import Base
import enum


# Enums
class DifficultyEnum(str, enum.Enum):
    easy = "easy"
    standard = "standard"


class MeasurementPreferenceEnum(str, enum.Enum):
    grams = "grams"
    ml = "ml"
    unit = "unit"
    calories = "kcal"


class MeasurementTypeEnum(str, enum.Enum):
    weight = "weight"
    volume = "volume"
    count = "count"


class SeasonEnum(str, enum.Enum):
    spring = "spring"
    summer = "summer"
    autumn = "autumn"
    winter = "winter"


# tables
class Country(Base):
    __tablename__ = "countries"
    code = Column(String, primary_key=True)
    name = Column(String)


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    recipes = relationship("RecipeTag", back_populates="tag")
