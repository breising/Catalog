from flask import Flask, redirect, render_template, url_for, request, \
    flash, jsonify
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import User, Base, Category, Item
import random
import string
from flask import session as login_session

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def signout():
    '''
    delete all the user data stored in the session
    '''

    login_session.clear()
    flash("Logged out.")

    active = "active"
    sign = "login"
    home = "active"
    delete = ""
    add = ""
    inout = "login"

    return redirect("/catalog?active=%s&sign=%s&home=%s&delete=%s"
                    "&add=%s&inout=%s"
                    % (active, sign, home, delete, add, inout))
