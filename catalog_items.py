from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import User, Base, Category, Item

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


user1 = User(name="breising", email="breising9@gmail.com")
user2 = User(name="Charls", email="breising2@gmail.com")
user3 = User(name="George", email="breising3@gmail.com")
session.add(user1)
session.add(user2)
session.add(user3)
session.commit()

category1 = Category(name="Frames", user_id=user1.id)
category2 = Category(name="Gruppos", user_id=user1.id)
category3 = Category(name="Wheels", user_id=user1.id)
category4 = Category(name="Tires", user_id=user1.id)
category5 = Category(name="Shifters", user_id=user1.id)
category6 = Category(name="Brakes", user_id=user1.id)
category7 = Category(name="Bars", user_id=user1.id)
category8 = Category(name="Cranks,chainrings", user_id=user3.id)
category10 = Category(name="Small parts", user_id=user3.id)


session.add(category1)
session.add(category2)
session.add(category3)
session.add(category4)
session.add(category5)
session.add(category6)
session.add(category6)
session.add(category7)
session.add(category8)
session.add(category10)


session.commit()

item1 = Item(name="Seven Ti road frame",
             description="Fully custom titanium road frame manf. "
             "by Seven in Boston",
             price="$4500.00",
             image="AurlGoesHere",
             sku="ab89349",
             user_id=2,
             category_id=2)
item2 = Item(name="SpeedVagen stock SS road frame",
             description="Stock road frame manf. by Vanilla Cycles, Portland",
             price="$2000.00",
             image="AurlGoesHere",
             sku="ab89779",
             user_id=3,
             category_id=3)
item3 = Item(name="Shimano Ultegra 6500 Sti",
             description="ten speed shifter, road",
             price="$350.00", image="AurlGoesHere", sku="ab89939",
             user_id=4,
             category_id=4)
#, category_id=category1, user_id=user1)

session.add(item1)
session.add(item2)
session.add(item3)
session.commit()

print "added menu items!"
