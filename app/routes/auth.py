from app.helpers.data import users
from app.helpers.format import user_dict
from app.routes import api

from flask import abort, redirect, render_template, request, session, url_for


@api.route('/login', methods=['GET'])
def render_login_page():
    return render_template('login.html')


@api.route('/login', methods=['POST'])
def authenticate():
    user_id = request.form.get('user_id')
    user = users.find_by_id(user_id)
    if not user:
        abort(401)

    session['user'] = user
    return redirect(url_for('api.render_dashboard'))

@api.route('/logout', methods=['GET'])
def logout():
    del session['user']
    return redirect(url_for('api.render_home'))