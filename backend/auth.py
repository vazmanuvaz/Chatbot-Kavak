from flask import session, redirect, url_for
import bcrypt

users = {}

def register_user(email, password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    users[email] = hashed

def login_user(email, password):
    hashed = users.get(email)
    if hashed and bcrypt.checkpw(password.encode(), hashed):
        session["user"] = email
        return True
    return False

def logout_user():
    session.clear()

def require_login(func):
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper
