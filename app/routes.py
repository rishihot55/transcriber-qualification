from flask import jsonify, abort, render_template, request
from app import app
from app.helpers import db

@app.route('/')
def render_leaderboard():
	return render_template('leaderboard.html')

@app.route('/items/', methods=['GET'])
def get_items():
	return jsonify(db.all('items'))

@app.route('/items/<int:id>', methods=['GET'])
def get_item(id):
	item = db.fetch('items', id)
	if item is None:
		abort(404)
	else:
		return jsonify(item)

@app.route('/items/', methods=['POST'])
def create_item():
	name = request.form['name']
	age = request.form['age']

	if name is None or age is None:
		abort(400)

	item = {'name': name, 'age': int(age)}
	db.insert('items', item)
	return jsonify(item)

@app.route('/items/<int:id>', methods=['PUT', 'PATCH'])
def update_item(id):
	name = request.form['name']
	age = request.form['age']

	item = db.fetch('items', id)
	if item is None:
		if name is None or age is None:
			abort(400)
		item = {'name': name, 'age': int(age)}
	else:
		if name is not None:
			item['name'] = name
		if age is not None:
			item['age'] = int(age)
		del item['id']
	db.update('items', item, id)
	item['id'] = id
	return jsonify(item)

@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
	item = db.remove('items', id)
	return jsonify(item if item is not None else {})

@app.route('/static/<path:path>')
def send_file(path):
	return send_from_directory('app/static', path)
