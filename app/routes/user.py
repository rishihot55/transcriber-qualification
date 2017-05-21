"""User Routes."""

from app.helpers.data import users
from app.helpers.decorators import admin
from app.helpers.forms import RegistrationForm
from app.routes import api

from flask import abort, jsonify, render_template, request


def parse_rights(admin, transcriber, voicer):
    return ''.join(['1' if p else '0' for p in [admin, transcriber, voicer]])


@api.route('/users/add', methods=['GET'])
def render_create_user():
    return render_template('users/create.html')


@api.route('/users', methods=['POST'])
@admin
def create_user():
    """Create User."""
    form = RegistrationForm(request.form)
    if not form.validate():
        abort(400)
    user = users.find_by_id(form.user_id.data)
    if user:
        abort(403)

    rights = parse_rights(form.admin, form.transcriber, form.voicer)
    user = users.add(form.user_id.data, rights, form.name.data, form.email.data)
    return jsonify(user)


@api.route('/users/<user_number>', methods=['PUT'])
@admin
def update_user(user_number):
    """
    Update User.

    Updates an existing user, otherwise creates a new user
    There is no requirement for a disable method since
    a disable is equivalent to removing all rights
    from a user
    """
    form = RegistrationForm(request.form)
    if not form.validate():
            abort(400)
    rights = parse_rights(form.admin, form.transcriber, form.voicer)
    user = users.find_by_number(user_number)
    if user:
        user = users.update(
            user_number, form.user_id.data, rights, form.name.data, form.email.data)
    else:
        user = users.add(
            form.user_id.data, rights, form.name.data, form.email.data)
    return jsonify(user)


@api.route('/users', methods=['GET'])
def get_all_users():
    user_list = users.all()
    return jsonify(user_list)


@api.route('/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = users.find_by_id(user_id)
    if not user:
        abort(404)
    return jsonify(user)