from functools import wraps
from flask import session, url_for, redirect

def user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('api.render_login_page'))
        return f(*args, **kwargs)
    return decorated_function

def admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or session['user']['rights'][0] == '0':
            return redirect(url_for('api.render_login_page'))
        return f(*args, **kwargs)
    return decorated_function


def transcriber(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or session['user']['rights'][1] == '0':
            return redirect(url_for('api.render_login_page'))
        return f(*args, **kwargs)
    return decorated_function


def voicer(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or session['user']['rights'][2] == '0':
            return redirect(url_for('api.render_login_page'))
        return f(*args, **kwargs)
    return decorated_function

def turker(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        pass
    return decorated_function