from flask import Flask, redirect, render_template, url_for, request, \
    flash, jsonify, make_response
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import User, Base, Category, Item
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
from functions import createUser, getUserID

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # This function responds to the ajax/post request made by the browser. The browser/client is attempting to send your app/server the token1 that it has just received from the G+ server.
    # First thing it does is Validate the state...get the state value from the post request sent by the browser. You'll find the {{state}} value was passed to the html page inside the <script> ajax ...so when the callback is called, now it's passing the {{state}} back to the app/server.
    # So, if state is not valid then send error response
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # If the state is valid, then Obtain G+ token1 from the get request
    code = request.data

    try:
        # Get the client secret stored in the server root dir as a .json file
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        # Upgrade the token into a credentials object
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # get the access token from the credentials object
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    # Check that the access token is valid.
    # "result" object contains the user info from the G+ server that you can now use to compare to the credentials object sent from the client
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    # check to see if the user is already authenticated .... that the user is
    # already stored in login_session
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    # login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # if user is not in the db ...
    user_id = getUserID(login_session['email'])
    if not user_id:
        # create the User in the local db by passing in the login_session
        # object
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    return redirect(url_for("main"))
