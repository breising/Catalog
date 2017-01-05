from flask import Flask, redirect, render_template, url_for, \
    request, flash, jsonify
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import User, Base, Category, Item
from flask import session as login_session
from dbSession import session

app = Flask(__name__)


@app.route('/catalog/JSON')
def catalogJSON(item_name, item_id):
    '''
   This function Responds to the get request to /caltalog/JSON with JSON formatted data containing all items in the db.
   '''
    if 'username' in login_session:
        item = session.query(Item).filter_by(id=item_id)
        return jsonify(CatalogItem=[i.serialize for i in item])
    # catergories = session.query(Category).all()
    return redirect('/login')
