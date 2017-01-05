from flask import Flask, redirect, flash
from flask import session as login_session


def signout():
    '''
    delete all the user data stored in the session
    '''
    login_session.clear()
    flash("Logged out.")

    active = "active"
    sign = "login"
    home = "active"
    delete = ""
    add = ""
    inout = "login"

    return redirect("/catalog?active=%s&sign=%s&home=%s&delete=%s"
                    "&add=%s&inout=%s"
                    % (active, sign, home, delete, add, inout))
