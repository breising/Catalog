from flask import Flask, redirect, render_template, url_for, request, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import User, Base, Category, Item

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def index():
    return redirect("/catalog/newArrivals", code=302)


@app.route('/catalog/<string:category_name>/', methods=['POST', 'GET'])
def main_login(category_name):
    # make the list of categories
    categories = session.query(Category).all()
    # make the list of items in the chosen category
    category = session.query(Category).filter_by(name=category_name).one()
    itemsInCategory = session.query(Item).filter_by(
        category_id=category.id).all()

    if request.method == 'POST':
        userName = request.form['userName']
        password = request.form['password']
        if userName and password:
            return redirect(url_for('main_user', userName=userName,
                                    category_name='newArrivals'))
        else:
            flash('Invalid username/password')
            return render_template('main_login.html', categories=categories,
                                   itemsInCategory=itemsInCategory, userName=userName,
                                   password=password)
    else:
        # else render the main page
        return render_template('main_login.html', categories=categories, itemsInCategory=itemsInCategory)


def valid_login(userName, password):
    return True


@app.route('/catalog/signup/', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        userName = request.form['userName']
        password = request.form['password']
        verify = request.form['verify']

        if userName and password and verify:
            if password == verify:
                flash("Welcome to the catalog.")
                return redirect(url_for('main_user', userName=userName,
                                        category_name='newArrivals'))
            else:
                flash("Passwords do not match")
                return render_template('signup.html')
        else:
            flash("Please provide all inputs")
            return render_template('signup.html')
    else:
        return render_template('signup.html')


@app.route('/catalog/<string:userName>/<string:category_name>/')
def main_user(userName, category_name):
    # first, make the list of categories
    categories = session.query(Category).all()

    # seond, make the list of items in the chosen category
    category = session.query(Category).filter_by(name=category_name).one()
    itemsInCategory = session.query(Item).filter_by(
        category_id=category.id).all()
    flash("Hi %s" % userName)
    return render_template('main_user.html', categories=categories,
                           itemsInCategory=itemsInCategory, userName=userName)

if __name__ == '__main__':
    app.secret_key = 'myVeryOwnSuperSecretKey'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
