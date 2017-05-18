from functools import wraps
from flask import session, url_for, redirect


def admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session['user']['rights'][0] == '0':
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def transcriber(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session['user']['rights'][1] == '0':
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def voicer(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session['user']['rights'][2] == '0':
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function