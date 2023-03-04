from sqlalchemy import Column, Integer, String, MetaData,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from config.db import engine



metadata = MetaData()
Base = declarative_base(metadata=metadata)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))

class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255))
    description = Column(String(255), unique=True, index=True)
    price = Column(Integer)

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255))
   
class GameCategory(Base):
    __tablename__ = "game_categories"
    game_id = Column(Integer, ForeignKey("games.id"), primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), primary_key=True, index=True)

metadata.create_all(bind=engine)