from flask import Blueprint

api = Blueprint('api', __name__)
from app.routes import admin, auth, base, data, hit, user
