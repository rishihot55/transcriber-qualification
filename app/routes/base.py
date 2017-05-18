from app.routes import api

from flask import render_template


@api.route('/', methods=['GET'])
def render_home():
    return render_template('home.html')


@api.route('/dashboard', methods=['GET'])
def render_dashboard():
    return render_template('dashboard.html')
