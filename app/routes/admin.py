from app.helpers.decorators import admin
from app.routes import api

from flask import render_template


@api.route('/admin', methods=['GET'])
@admin
def render_admin_panel():
    return render_template('admin.html')
