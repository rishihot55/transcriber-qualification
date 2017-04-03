from flask import jsonify, abort, render_template, request
from app import app
from app.helpers import db, order, cast, top_n

@app.route('/')
def render_leaderboard():
	return render_template('leaderboard.html')

@app.route('/items/', methods=['GET'])
def get_items():
	limit = request.args.get('limit')
	limit = 30 if limit is None else int(limit)
	
	order_key = request.args.get('orderby')
	order_direction = request.args.get('order_dir')

	filter_key = request.args.get('filterby')
	filter_value = request.args.get('filtervalue')

	items = db.all('items')
	if order_key in ['name', 'url', 'valid']:
		items = order(items, order_key, order_direction)

	if filter_key in ['name', 'url', 'valid']:
		value = cast('items', value, filter_key)
		items = [item for item in items if item[filter_key] == value]

	items = top_n(items, limit)
	return jsonify(items)

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
