import functools
from typing import Callable
from flask import session, flash, redirect, url_for, current_app

def requires_login(func: Callable) -> Callable:
    @functools.wraps(func)
    def decorated_function(*args, **kwargs):
        if not session.get("email"):
            flash("You need to be signed in for this page.", "danger")
            return redirect(url_for("users.login_user"))
        return func(*args, **kwargs)
    return decorated_function

def requires_admin(func: Callable) -> Callable:
    @functools.wraps(func)
    def decorated_function(*args, **kwargs):
        if session.get("email") != current_app.config.get("ADMIN", ""): #If there is no admin use empty string instead
            flash("You need to be administrator to access this page", "danger")
            return redirect(url_for("users.login_user"))
        return func(*args, **kwargs)
    return decorated_function
