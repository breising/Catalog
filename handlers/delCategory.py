from flask import Flask, redirect, render_template, url_for, request, \
    flash, jsonify
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import User, Base, Category, Item
from flask import session as login_session
from dbSession import session


def delCategory(category_name, category_id):
    '''
    GET: renders the delCategory.html page
    POST: deletes the selected category
    '''
    # get all the categories to create the list
    categories = session.query(Category).all()

    # is the user logged in ?
    if 'email' in login_session:
        # if loginsession:user_id is equal to the item's user_id(author) then
        # the logged in user is the author so allow access to edit
        if request.method == 'POST':
            # get the selected category from the form
            cat_id = request.form['categoryId']
            # the category author must match the users id
            # get the data field values from the post request
            deleteThis = session.query(Category).filter_by(id=cat_id).one()
            del_author = deleteThis.user_id

            if del_author != login_session['user_id']:
                flash("You are not the author, no can do.")
                return render_template('delCategory.html',
                                       category_name=category_name,
                                       category_id=category_id,
                                       categories=categories)

            cat_name = deleteThis.name
            # delete all the items in this category also
            deleteItems = session.query(Item).filter_by(
                category_id=cat_id).all()
            # iterate through all the items and delete each one.
            for x in deleteItems:
                session.delete(x)
                session.commit()

            # now delete the category
            session.delete(deleteThis)
            session.commit()

            flash("Category %s was deleted along with all its items."
                  % (cat_name))
            active = "active"
            sign = "Out"
            home = "active"
            delete = ""
            add = ""
            inout = "signout"

            # return url_for("main")

            return redirect(
                "/catalog?active=%s&sign=%s&home=%s&delete=%s&add=%s&inout=%s"
                % (active, sign, home, delete, add, inout))

        else:
            active = "active"
            sign = "logout"
            home = ""
            delete = "active"
            add = ""
            inout = "signout"
            return render_template('delCategory.html',
                                   category_name=category_name,
                                   category_id=category_id,
                                   categories=categories,
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
        flash('You must be logged in to delete a category.')
        return redirect(
            "/catalog/%s/items/%s?active=%s&sign=%s&home=%s&delete="
            "%s&add=%s&inout=%s"
            % (category_name, category_id, active, sign, home,
                delete, add, inout))
