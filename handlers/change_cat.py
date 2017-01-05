from flask import Flask, redirect, render_template, flash, jsonify
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import User, Base, Category, Item
from flask import session as login_session
from dbSession import session

app = Flask(__name__)


def change_cat(category_name, category_id):
    '''
    GET: renders the main page with the newly selected category
    '''
    # get all the categories from db
    categories = session.query(Category).all()
    # get all items that have "category_id"
    item_list = session.query(Item).filter_by(
        category_id=category_id).all()
    # count the items that have "category_id"
    item_count = session.query(Item).filter_by(category_id=category_id).count()
    list_title = category_name
    # before rendering page, check auth first and redirect to / if not

    if 'email' in login_session:
        user_email = login_session['email']
        active = "active"
        sign = "logout"
        home = "active"
        delete = ""
        add = ""
        inout = "signout"
        return render_template('main_auth.html', categories=categories,
                               item_list=item_list,
                               user_email=user_email,
                               category_name=category_name,
                               item_count=item_count,
                               category_id=category_id,
                               active=active,
                               sign=sign,
                               home=home,
                               delete=delete,
                               add=add,
                               inout=inout,
                               list_title=list_title)
    else:
        active = "active"
        sign = "login"
        home = "active"
        delete = ""
        add = ""
        inout = "login"
        return render_template('main.html', categories=categories,
                               item_list=item_list,
                               category_name=category_name,
                               item_count=item_count,
                               category_id=category_id,
                               active=active,
                               sign=sign,
                               home=home,
                               delete=delete,
                               add=add,
                               inout=inout,
                               list_title=list_title)
