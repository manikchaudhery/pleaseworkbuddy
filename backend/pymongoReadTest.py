from pymongo import MongoClient
client = MongoClient('localhost', 27017)

db = client['CSC326_Database']
invertedIndexDB = db['Inverted_Index']

posts = invertedIndexDB.find({'word_id': 6})

for post in posts:
    print(post)
    test = post['doc_IDs']
    print test
    for num in test:
    	print num