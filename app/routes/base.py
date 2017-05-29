from app.routes import api

from flask import render_template, send_from_directory


@api.route('/', methods=['GET'])
def render_home():
    return render_template('home.html')


@api.route('/dashboard', methods=['GET'])
def render_dashboard():
    return render_template('dashboard.html')


@api.route('/js/<path:path>', methods=['GET'])
def send_js_files(path):
    return send_from_directory('resources/js', path)