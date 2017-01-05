from flask import Flask, redirect, render_template, url_for, request, flash, jsonify
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import User, Base, Category, Item
from flask import session as login_session


# app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def createUser(login_session):
    '''
    THis fx accesses information about the user that is stored in login_session and was gotten from the G+ server, their email, username and uses that info to create a User in our system db. So we'll have our user's basic info stored on our system to use for authorizing various activities like creating Items and Categories etc. but we'll NOT have their password. And we won't have to worry about managing passwords.
    '''
    # is the user already in the db ?
    alreadyUser = session.query(User).filter_by(email=login_session['email']).\
        one()
    # if so, don't add it again
    if alreadyUser.email:
        print "Your email is already in the database."
        return alreadyUser.id
    # if not then add it
    else:
        newUser = User(name=login_session['username'], email=login_session[
                       'email'])
        session.add(newUser)
        session.commit()

    try:
        user = session.query(User).filter_by(email=login_session['email']).\
            one()
        return user.id
    except:
        print "CreateUser failed on something."
