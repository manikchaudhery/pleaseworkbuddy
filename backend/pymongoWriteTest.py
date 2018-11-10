# from pymongo import MongoClient
# client = MongoClient('localhost', 27017)

# db = client.pymongo_test

# test = db.test

from collections import defaultdict

index = defaultdict(set)
index[1] = {1,2,3,4,5,6,7,8,9,10}
index[2] = {11,12,13,14,15,16,17}

print "START"

for id in index:
	print id, index[id]
# post_data = {
#     'title': 'Python and MongoDB',
#     'content': 'PyMongo is fun, you guys',
#     'author': 'Scott'
# }
# result = test.insert_one(post_data)
# print('One post: {0}'.format(result.inserted_id))

# post_1 = {
#     'title': 'Python and MongoDB',
#     'content': 'PyMongo is fun, you guys',
#     'author': 'Scott'
# }
# post_2 = {
#     'title': 'Virtual Environments',
#     'content': 'Use virtual environments, you guys',
#     'author': 'Scott'
# }
# post_3 = {
#     'title': 'Learning Python',
#     'content': 'Learn Python, it is easy',
#     'author': 'Bill'
# }
# new_result = test.insert_many([post_1, post_2, post_3])
# print('Multiple posts: {0}'.format(new_result.inserted_ids))