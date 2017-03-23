import pickle
import os.path
from collections import OrderedDict

data_file = 'db.pkl'

seed_data = {
	'items': OrderedDict([
		(1, {'name': 'Rishi', 'age': 200 }), 
		(2, {'name': 'Raj', 'age': 21 })
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

def tag(item, id):
		item['id'] = id
		return item

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