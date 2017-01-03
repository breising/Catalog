from flask import Flask, redirect, render_template, url_for, request, \
    flash, jsonify, make_response
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import User, Base, Category, Item
from handlers import main, login, item_detail, item_edit, change_cat,\
    item_delete, add_item, signout, delCategory, catalogJSON, gconnect, gdisconnect
import string
from flask import session as login_session

APPLICATION_NAME = "Catalog"

app = Flask(__name__)

# prevent a CSRF attack by putting secret in the forms
app.secret_key = 'brisIsblah7823andalsoisbiablai'

# KEEP email config code below for use with the contact form
# app.config["MAIL_SERVER"] = "mail.orthocure.biz"
# app.config["MAIL_PORT"] = 465
# app.config["MAIL_USE_TLS"] = False
# app.config["MAIL_USE_SSL"] = True
# app.config["MAIL_USERNAME"] = 'support@orthocure.biz'
# app.config["MAIL_PASSWORD"] = 'Bcr062003'

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Handlers
# redirect all / requests to /catalog


@app.route('/')
def redirCatalog():
    return redirect('/catalog')

# refactored the remaining handlers to reference handlers in modules

main = app.route\
    ('/catalog', methods=['GET', 'POST'])(main)


login = app.route\
    ('/catalog/login/', methods=['GET', 'POST'])(login)

item_detail = app.route\
    ('/catalog/item/<string:item_name>/<string:item_id>')(item_detail)

item_edit = app.route\
    ('/catalog/item/<string:item_name>/<string:item_id>/edit',
     methods=['GET', 'POST'])(item_edit)

item_delete = app.route\
    ('/catalog/item/<string:item_name>/<string:item_id>/delete',
     methods=['GET', 'POST'])(item_delete)

change_cat = app.route\
    ('/catalog/<string:category_name>/items/<int:category_id>')(change_cat)

add_item = app.route\
    ('/catalog/add-item/<string:category_name>/<int:category_id>',
     methods=['GET', 'POST'])(add_item)

signout = app.route\
    ('/catalog/signout')(signout)

delCategory = app.route\
    ('/catalog/deleteCategory/<string:category_name>/<int:category_id>',
     methods=['GET', 'POST'])(delCategory)

catalogJSON = app.route\
    ('/catalog/JSON')(catalogJSON)

gconnect = app.route\
    ('/gconnect', methods=['POST'])(gconnect)

gdisconnect = app.route\
    ('/gdisconnect')(gdisconnect)


if __name__ == '__main__':
    app.secret_key = 'brisIsblah7823andalsoisbiablai'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

'''
Keep this code for later implementation. Already troubleshooted the email functionality.

@app.route('/contact', methods=['POST', 'GET'])
def contact():
    form = ContactForm()

    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('contact.html', form=form)
        else:
            email = form.email
            msg = Message(form.subject.data, sender="support@orthocure.biz",
                          recipients=['support@orthocure.biz'])
            msg.body = """
            From: %s <%s>
            %s
            """ % (form.name.data, form.email.data, form.message.data)
            mail.send(msg)

            return render_template('contact.html', success=True)

    elif request.method == 'GET':
        return render_template('contact.html', form=form)
'''
