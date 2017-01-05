from flask import Flask, redirect, render_template, url_for, request, \
    flash, jsonify
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import User, Base, Category, Item
from flask import session as login_session
from dbSession import session


def main():
    '''
    GET: render main_auth.html if auth...  or main.html if not

    '''
    # make the list of categories
    categories = session.query(Category).all()
    # get list of 10 most recently created items
    item_list = session.query(Item).order_by(desc('created')).limit(10).all()
    # count the items
    item_count = session.query(Item).order_by(
        desc('created')).limit(10).count()

    # set name of the list title rather than using the category name
    list_title = "New Arrivals"
    # active sets the blue highlight of the selected category list
    active = "active"
    # sign is the label for the menu
    sign = "logout"
    # main menu set which tab is active
    home = "active"
    delete = ""
    add = ""
    # set cat name to None in cases where the list_title is not set
    category_name = "None"
    category_id = 0

    if 'email' in login_session:
        user_email = login_session['email']
        # inout is the var used in the url for the login/out tab on the main
        # menu
        inout = "signout"
        return render_template('main_auth.html',
                               categories=categories,
                               category_name=category_name,
                               category_id=category_id,
                               item_list=item_list,
                               user_email=user_email,
                               item_count=item_count,
                               active=active,
                               sign=sign,
                               home=home,
                               delete=delete,
                               add=add,
                               inout=inout,
                               list_title=list_title)
    else:
        # inout is the var used in the url for the login/out tab on the main
        # menu
        inout = "login"
        # sign is the label for the main menu
        sign = "login"
        return render_template('main.html',
                               categories=categories,
                               category_name=category_name,
                               category_id=category_id,
                               item_list=item_list,
                               item_count=item_count,
                               active=active,
                               sign=sign,
                               home=home,
                               delete=delete,
                               add=add,
                               inout=inout,
                               list_title=list_title)
