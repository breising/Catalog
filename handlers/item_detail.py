from flask import Flask, redirect, render_template, url_for, request, \
    flash, jsonify
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import User, Base, Category, Item
from flask import session as login_session
from dbSession import session


def item_detail(item_name, item_id):
    # query the db to get the item object by id
    item = session.query(Item).filter_by(id=item_id).one()
    category = session.query(Category).filter_by(id=item.category_id).one()
    category_name = category.name
    category_id = category.id

    # authenticate before rendering

    if 'email' in login_session:
        print login_session['user_id']
        print item.user_id
        # if the user is the author of the item, then show the edit and delete
        # buttons (flag = 'inline-block') ...if not don't show (flag = 'none' )
        if login_session['user_id'] == item.user_id:
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
            url_delete = "/catalog/item/%s/%s/delete" % (
                item.name, item_id)
            # get the item
            item = session.query(Item).filter_by(id=item_id).one()
            # the item's author is the user_id
            author_id = item.user_id
            # get the author name
            author = session.query(User).filter_by(id=author_id).one()
            auth_name = author.name

            active = "active"
            sign = "Out"
            home = "active"
            delete = ""
            add = ""
            inout = "signout"
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
                                   inout=inout,
                                   auth_name=auth_name)
        else:
            flag = 'none'
            url_edit = ''
            url_delete = ''
            user_email = ''
            active = "active"
            sign = "Out"
            home = "active"
            delete = ""
            add = ""
            inout = "signout"
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
    else:
        flag = 'none'
        url_edit = ''
        url_delete = ''
        user_email = ''
        active = "active"
        sign = "Login"
        home = "active"
        delete = ""
        add = ""
        inout = "login"
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
