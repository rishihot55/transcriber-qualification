import pickle
import os.path
from collections import OrderedDict

data_file = 'db.pkl'

seed_data = {
	'items': OrderedDict([
		(1, {
				'name': 'Pronounciation Exemplar',
				'url': 'http://talknicer.com/recdemo/',
				'valid': True
		}), 
		(2, {
				'name': 'Transcriber Exemplar',
				'url': 'https://rrajasek95.pythonanywhere.com',
				'valid': False
		})
	])
}

data = None
if os.path.exists('data_file'):
	with open(data_file, 'rb') as f:
		data = pickle.load(f)
else:
	with open(data_file, 'wb') as f:
		data = seed_data
		pickle.dump(data, f)

def order(items, key, order_direction):
	reverse_dir = order_direction == 'desc'
	return sorted(items, key=lambda item: item[key], reverse=reverse_dir)

def tag(item, id):
		item['id'] = id
		return item

def top_n(items, limit='30'):

	items = items if len(items) < limit else items[:limit]
	return items

# identity function, used for performing a default cast
def id(x):
	return x

def bool(x):
	return x in ['true']

def cast(table, key, value):
	func_dict = {
		'items': {
			'name': id,
			'url': id,
			'valid': bool
		}
	}

	return func_dict[table][key](value)

class Database():
	def __init__(self, data):
		self.__data = data

	def fetch(self, table, id):
		if id in self.__data[table]:
			item = self.__data[table][id]
			return tag(item, id)
		else:
			return None

	def all(self, table):
		return [tag(self.__data[table][id], id) for id in self.__data[table]]

	def get_filtered(self, table, predicate):
		tagged_items = all(table)
		filtered_items = [item for item in tagged_items if predicate(item)]
		return filtered_items

	def remove(self, table, id):
		if id in self.__data[table]:
			item = self.__data[table].pop(id)
			self.commit()
			return tag(item, id)
		return None

	def commit(self):
		with open(data_file, 'wb') as f:
			pickle.dump(self.__data, f)

	def max_index(self, table):
		return max(self.__data[table].keys())

	def count(self, table):
		return len(self.__data[table])

	def insert(self, table, item):
		new_id = self.max_index(table) + 1
		self.__data[table][new_id] = item
		self.commit()

	def update(self, table, item, id):
		self.__data[table][id] = item
		self.commit()

db = Database(data)