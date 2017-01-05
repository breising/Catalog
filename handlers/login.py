from flask import Flask, redirect, render_template, url_for, request, \
    flash, jsonify
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import User, Base, Category, Item
import random
import string
from flask import session as login_session
from dbSession import session


def login():
    '''
    Get: render login.html

    '''
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state

    active = "active"
    sign = "login"
    home = "active"
    delete = ""
    add = ""
    inout = "login"

    return render_template('login.html',
                           state=state,
                           active=active,
                           sign=sign,
                           home=home,
                           delete=delete,
                           add=add,
                           inout=inout)
