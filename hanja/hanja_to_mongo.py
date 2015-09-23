'''
This file just loads the hanja into mongo...
'''

from pymongo import MongoClient
from bson.objectid import ObjectId
client = MongoClient('mongodb://localhost:27017/')

db_name = 'hanja'

db = client[db_name]
collection = db[db_name]

def insert_hanja_into_mongo():
	hanja_json_dict = {
	      '8':   'hanja_8.json',
	        '7':   'hanja_7.json',
	        '6-1': 'hanja_6-1.json',
	        '6-2': 'hanja_6-2.json',
	        '5-1': 'hanja_5-1.json',
	        '5-2': 'hanja_5-2.json',
	        '4-1': 'hanja_4-1.json',
	        '4-2': 'hanja_4-2.json',
	        '3-1': 'hanja_3-1.json',
	        '3-2': 'hanja_3-2.json',
	        '2-2': 'hanja_2-2.json',
	        '2-1': 'hanja_2-1.json',
	        '1': 'hanja_1.json'
	}
	import json, os
	new_posts = []
	APP_ROOT = os.path.dirname(os.path.abspath(__file__))
	for hanja_level in hanja_json_dict:
		filename = hanja_json_dict[hanja_level]
		with open(filename) as outfile:
			data = json.load(outfile)
		new_posts.append({hanja_level: data})
	print(new_posts)
	hanja = db.hanja
	result = hanja.insert_many(new_posts)

def insert_articles_into_mongo():
	import json, os
	new_posts = []
	APP_ROOT = os.path.dirname(os.path.abspath(__file__))
	ARTICLE_FOLDER = os.path.join(APP_ROOT, 'articles')
	with open(os.path.join(ARTICLE_FOLDER, 'articles.json')) as outfile:
		data = json.load(outfile)
	print(data)
	article_collection = db.articles
	for source in data:
		filename = data[source]['link']
		if article_collection.find_one({"link": filename}) is None:
			entry = {'link': filename}
			text = ''
			with open(os.path.join(ARTICLE_FOLDER, filename), encoding="utf-8") as outfile:
				text = outfile.read()
			entry['text'] = text
			entry['source'] = data[source]['source']
			article_collection.insert_one(entry)

def update_article_hanja_count():
	article_collection = db.articles
	for article in article_collection.find():
		if 'hanja_count' not in article:
			update_entry(article_collection, article['_id'], {"hanja_count": hanja_count_for_text(article['text'])})

def hanja_count_for_text(text):
	result_dict = {}
	for chararacter in text:
		for hanja in db.hanja.find():
			for key in hanja:
				if key != '_id':
					for char in hanja[key]:
						if chararacter in char['字']:
							if key not in result_dict:
								result_dict[key] = {'count': 0, 'chars': []}
							result_dict[key]['count'] += 1
							if chararacter not in result_dict[key]['chars']:
								result_dict[key]['chars'].append(chararacter)
	return result_dict

def update_entry(collection, id, dict):
	collection.update_one(
	    {"_id": id},
	    {"$set": dict}
	)

def get_article(id):
	article_collection = db.articles
	return article_collection.find_one({'_id': ObjectId(id)})

def get_all_articles():
	article_collection = db.articles
	result = []
	for article in article_collection.find():
		result.append(article)
	return result

article_collection = db.articles
print(article_collection.find_one())