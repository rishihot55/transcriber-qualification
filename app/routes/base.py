from app.routes import api

from flask import redirect, render_template, send_from_directory, session
from app.helpers.decorators import user


@api.route('/', methods=['GET'])
def render_home():
    return render_template('home.html')


@api.route('/dashboard', methods=['GET'])
@user
def render_dashboard():
    if session['user']['rights'][1] == '1':
        return redirect('/transcripts')

    return render_template('dashboard.html')


@api.route('/js/<path:path>', methods=['GET'])
def send_js_files(path):
    return send_from_directory('resources/js', path)
