from flask import Flask, redirect, render_template, url_for, \
    request, flash, jsonify
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import User, Base, Category, Item
from flask import session as login_session


app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/catalog/JSON')
def catalogJSON():
    '''
   This function Responds to the get request to /caltalog/JSON with JSON formatted data containing all items in the db.
   '''
    if 'username' not in login_session:
        return redirect('/login')
    # catergories = session.query(Category).all()
    items = session.query(Item).all()
    return jsonify(CatalogItems=[i.serialize for i in items])
