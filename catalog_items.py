from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import User, Base, Category, Item

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Menu for UrbanBurger
user1 = User(name="Brian")
user2 = User(name="Charls")
user3 = User(name="George")
session.add(user1)
session.add(user2)
session.add(user3)
session.commit()

category1 = Category(name="Frames", author=user2.id)
category2 = Category(name="Gruppos", author=user2.id)
category3 = Category(name="Wheels", author=user2.id)
category4 = Category(name="Tires", author=user2.id)
category5 = Category(name="Shifters", author=user2.id)
category6 = Category(name="Brakes", author=user2.id)
category7 = Category(name="Bars", author=user2.id)
category8 = Category(name="Cranks,chainrings", author=user2.id)
category9 = Category(name="Cranks,chainrings", author=user2.id)
category10 = Category(name="Small parts", author=user2.id)
category11 = Category(name="newArrivals", author=user1.id)

session.add(category1)
session.add(category2)
session.add(category3)
session.add(category4)
session.add(category5)
session.add(category6)
session.add(category6)
session.add(category7)
session.add(category8)
session.add(category9)
session.add(category10)
session.add(category11)

session.commit()

item1 = Item(name="Seven Ti road frame",
             description="Fully custom titanium road frame manf. by Seven in Boston",
             price="$4500.00", image="AurlGoesHere", sku="ab89349",
             author=user1.id,
             category_id=category10.id)
item2 = Item(name="SpeedVagen stock SS road frame",
             description="Stock road frame manf. by Vanilla Cycles, Portland",
             price="$2000.00", image="AurlGoesHere", sku="ab89779",
             author=user2.id,
             category_id=category10.id)
item3 = Item(name="Shimano Ultegra 6500 Sti",
             description="ten speed shifter, road",
             price="$350.00", image="AurlGoesHere", sku="ab89939",
             author=user3.id,
             category_id=category10.id)
#, category_id=category1, author=user1)

session.add(item1)
session.add(item2)
session.add(item3)
session.commit()

print "added menu items!"
