from flask import Flask, redirect, render_template, url_for, request, \
    flash, jsonify
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import User, Base, Category, Item
from flask import session as login_session
from dbSession import session


def item_delete(item_name, item_id):
    '''
    GET : render the item_delete.html page
    POST : deletes the 
    '''
    # get all the needed data: cat name and id, item name and id
    item = session.query(Item).filter_by(id=item_id).one()
    category = session.query(Category).filter_by(id=item.category_id).one()
    category_name = category.name
    category_id = category.id
    # flag is used in the html template to toggle display of the edit and
    # delete tags based on user athentication
    flag = 'inline-block'
    # pass the user email into the html template to acknowledge auth
    # status
    user_email = login_session['email']
    # use these urls to pass into the html dock, if user is not
    # authenticated, then they cannot see the url for editing or
    # deleting
    url_edit = "/catalog/item/%s/%s/edit" % (item.name, item_id)
    url_delete = "/catalog/item/%s/%s/delete" % (item.name, item_id)
    # is the user logged in ?
    if login_session['email']:
        # if loginsession:user_id is equal to the item's user_id(author) then
        # the logged in user is the author so allow access to edit
        if login_session['user_id'] == item.user_id:
            if request.method == 'POST':

                # get the data field values from the post request
                ditem = session.query(Item).filter_by(id=item_id).one()

                session.delete(ditem)
                flash("Item %s in %s was deleted." %
                      (item_name, category_name))
                # save info to db
                session.commit()

                active = "active"
                sign = "Out"
                home = "active"
                delete = ""
                add = ""
                inout = "signout"

                return redirect("/catalog/%s/items/%s?active=%s&sign=%s"
                                "&home=%s&delete=%s&add=%s&inout=%s"
                                % (category_name, category_id, active, sign,
                                   home, delete, add, inout))
            # GET request...confirm deletions
            else:
                active = "active"
                sign = "Out"
                home = "active"
                delete = ""
                add = ""
                inout = "signout"
                flash("Delete this item?")
                return render_template('item_delete.html', item=item,
                                       user_email=user_email,
                                       category_name=category_name,
                                       category_id=category_id,
                                       active=active,
                                       sign=sign,
                                       home=home,
                                       delete=delete,
                                       add=add,
                                       inout=inout)
        # user id not the author
        else:
            active = "active"
            sign = "Out"
            home = "active"
            delete = ""
            add = ""
            inout = "signout"
            flash('You must be the auther to edit an item.')
            return render_template('item_detail.html', item=item,
                                   user_email=user_email,
                                   category_name=category_name,
                                   category_id=category_id,
                                   flag=flag,
                                   url_edit=url_edit,
                                   url_delete=url_delete,
                                   active=active,
                                   sign=sign,
                                   home=home,
                                   delete=delete,
                                   add=add,
                                   inout=inout)
    # user is not logged in
    else:
        active = "active"
        sign = "Out"
        home = "active"
        delete = ""
        add = ""
        inout = "login"
        flash('You must be logged in as the auther to edit an item.')
        return render_template('item_detail.html', item=item,
                               user_email=user_email,
                               category_name=category_name,
                               category_id=category_id,
                               flag=flag,
                               url_edit=url_edit,
                               url_delete=url_delete,
                               active=active,
                               sign=sign,
                               home=home,
                               delete=delete,
                               add=add,
                               inout=inout)
