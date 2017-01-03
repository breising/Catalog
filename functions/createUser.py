from flask import Flask, redirect, render_template, url_for, request, flash, jsonify
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import User, Base, Category, Item
from flask import session as login_session


app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def createUser(login_session):
    '''
    THis fx accesses information about the user that is stored in login_session and was gotten from the G+ server, their email, username and uses that info to create a User in our system db. So we'll have our user's basic info stored on our system to use for authorizing various activities like creating Items and Categories etc. but we'll NOT have their password. And we won't have to worry about managing passwords.
    '''
    newUser = User(name=login_session['username'], email=login_session[
                   'email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    '''
    This function uses the user_id parameter to query the db for the current user row object and returns that object.

    '''
    user = session.query(User).filter_by(id=user_id).one()
    # returns the whole user object
    return user
