from flask import Flask, redirect, render_template, url_for, request,\
    flash, jsonify
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import User, Base, Category, Item
from flask import session as login_session


app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def add_item(category_name, category_id):
    '''
    GET renders the add-item html page with all its needed data
    POST saves the new item in the db
    '''
    # get the category list
    categories = session.query(Category).all()
    # get all the items in the category
    item_list = session.query(Item).filter_by(category_id=category_id).all()
    # count all the items in the category
    item_count = session.query(Item).filter_by(category_id=category_id).count()
    # before rendering page, check auth first and redirect to / if not
    if 'email' in login_session:
        user_email = login_session['email']
        if request.method == 'POST':
            # get the data from the post request
            name = request.form['name']
            description = request.form['description']
            price = request.form['price']
            image = request.form['image']
            sku = request.form['sku']
            user_id = login_session['user_id']
            cat_id = request.form['categoryId']

            # if user selects to add a new category then ...
            if cat_id == "* add new":
                print("IF here!")
                # get the new cat name from the form
                newCategory = request.form['newCategory']
                # does the category already exist
                is_already_category = session.query(
                    Category).filter_by(name=newCategory).count()
                # check if the category already exists
                if is_already_category > 0:
                    flash("Category already exists.")
                    return render_template('add-item.html',
                                           categories=categories)
                else:
                    # record the new category in the db
                    cat = Category(name=newCategory,
                                   user_id=login_session['user_id'])
                    session.add(cat)
                    session.commit()
                    # get the id of the new category
                    new_cat_id = session.query(
                        Category).filter_by(name=newCategory).one()
                    new_cat_id = new_cat_id.id

                    # add new item with the new category id
                    item = Item(name=name,
                                description=description,
                                price=price,
                                image=image,
                                sku=sku,
                                user_id=user_id,
                                category_id=new_cat_id)
                    session.add(item)
                    session.commit()

                    cat_name = session.query(
                        Category).filter_by(id=new_cat_id).one()

                    flash("Item '%s' was added to category '%s'"
                          % (name, newCategory))
                    return redirect("/catalog/%s/items/%s"
                                    % (category_name, category_id))
            else:
                # add new item the selected existing category
                item = Item(name=name,
                            description=description,
                            price=price,
                            image=image,
                            sku=sku,
                            user_id=user_id,
                            category_id=cat_id)
                session.add(item)
                session.commit()

                cat_name = session.query(Category).filter_by(id=cat_id).one()

                flash("Item '%s' was added to category '%s'"
                      % (name,
                         cat_name.name))
                active = "active"
                sign = "logout"
                home = "active"
                delete = ""
                add = ""
                inout = "signout"
                return redirect("/catalog/%s/items/%s?active=%s&sign=%s\
                    &home=%s&delete=%s&add=%s&inout=%s"
                                % (category_name, category_id, active, sign, home, delete, add, inout))

        else:
            # get all categories for the drop down list
            active = "active"
            sign = "logout"
            home = ""
            delete = ""
            add = "active"
            inout = "signout"
            return render_template('add-item.html', categories=categories,
                                   category_name=category_name,
                                   category_id=category_id,
                                   active=active,
                                   sign=sign,
                                   home=home,
                                   delete=delete,
                                   add=add,
                                   inout=inout)
    else:
        active = "active"
        sign = "Login"
        home = "active"
        delete = ""
        add = ""
        inout = "login"
        flash("You must login to add an item.")
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
                               inout=inout)
