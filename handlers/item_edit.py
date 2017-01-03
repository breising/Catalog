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


def item_edit(item_name, item_id):
    '''
    GET: render edit-item.html if user logged in and if author
    POST: record changes
    '''

    item = session.query(Item).filter_by(id=item_id).one()
    category = session.query(Category).filter_by(id=item.category_id).one()
    category_name = category.name
    category_id = category.id

    # is the user logged in ?
    if 'email' in login_session:
        user_email = login_session['email']
        # if loginsession:user_id is equal to the item's user_id(author) then
        # the logged in user is the author so allow access to edit
        if login_session['user_id'] == item.user_id:
            if request.method == 'POST':
                # get the data field values from the post request
                name = request.form['name']
                description = request.form['description']
                image = request.form['image']
                sku = request.form['sku']
                # assign values to the db object properties
                item.name = name
                item.description = description
                item.image = image
                item.sku = sku
                # save info to db
                session.commit()

                flash("Edit was successful.")
                return render_template('item_detail.html', item=item,
                                       user_email=user_email,
                                       category_name=category_name,
                                       category_id=category_id)
            else:

                return render_template('item_edit.html', item=item,
                                       user_email=user_email,
                                       category_name=category_name,
                                       category_id=category_id)
        else:
            flash('You must be logged in as the auther to edit an item.')
            return render_template('item_detail.html', item=item,
                                   user_email=user_email,
                                   category_name=category_name,
                                   category_id=category_id)
    else:
        flash('You must be logged in as the auther to edit an item.')
        return render_template('item_detail.html', item=item,
                               user_email=user_email,
                               category_name=category_name,
                               category_id=category_id)
