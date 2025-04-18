from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True)
    email = Column(String, unique=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    password = Column(String)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    country_code = Column(String, ForeignKey("countries.code"))
    country = relationship("countries", back_populates="users")
    recipes = relationship("Recipe", back_populates="creator")


class Favorite(Base):
    __tablename__ = "favorites"
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id))
    recipe_id = Column(UUID(as_uuid=True), ForeignKey("recipes.id"))
    liked = Column(Boolean)
    made_it = Column(Boolean)
    rating = Column(Integer)


class RecipeView(Base):
    __tablename__ = "recipe_views"
    id = Column(Integer, primary_key=True)
    recipe_id = Column(UUID(as_uuid=True), ForeignKey("recipes.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    viewed_at = Column(DateTime, default=datetime.now)


class UserTags(Base):
    __tablename__ = "user_tags"
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)
    user = relationship("User", back_populates="tags")
