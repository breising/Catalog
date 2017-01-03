import os
import datetime
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, desc

Base = declarative_base()

# if you make changes in the future to the tables below then:
# first delete the existing "catalog.db" file in the root of catalog
# then, from the catalog root: run this file via: python database_setup.py
# to create a new "catalog.db" file that has the new changes.


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


class Item(Base):
    __tablename__ = 'item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    image = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    sku = Column(String(80))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    created = Column(DateTime, default=datetime.datetime.utcnow)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'image': self.image,
            'sku': self.sku
        }

engine = create_engine('sqlite:///catalog.db')


Base.metadata.create_all(engine)
