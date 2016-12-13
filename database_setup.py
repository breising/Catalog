import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# if you make changes in the future to the tables below then:
# first delete the existing "catalog.db" file in the root of catalog
# then, from the catalog root: run this file via: python database_setup.py
# to create a new "catalog.db" file that has the new changes.


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    author = Column(String(80), ForeignKey('user.id'))


class Item(Base):
    __tablename__ = 'item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    image = Column(String(250))
    category_id = Column(String(80), ForeignKey('category.id'))
    sku = Column(String(80))
    author = Column(String(80), ForeignKey('user.id'))


engine = create_engine('sqlite:///catalog.db')


Base.metadata.create_all(engine)
