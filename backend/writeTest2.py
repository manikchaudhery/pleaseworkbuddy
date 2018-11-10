from collections import defaultdict
from pymongo import MongoClient
client = MongoClient('localhost', 27017)

db = client.WriteToSet

collection1 = db.collection1

index = defaultdict(set)
index[1] = {1,2,3,4,5,6,7,8,9,10}
index[2] = {11,12,13,14,15,16,17}
print list(index[1])[9]
print "START"

for id in index:
    print id, index[id]
    data = {
        'index': id,
        'set': []
    }
    collection1.insert_one(data)

    for i in range(len(index[id])):
        print i
        collection1.update(
                            {
                                'index': id
                            },
                            {
                                '$push': {'set': list(index[id])[i]}
                            })




post_1 = {
    'title': 'Python and MongoDB',
    'content': 'PyMongo is fun, you guys',
    'author': 'Scott'
}
post_2 = {
    'title': 'Virtual Environments',
    'content': 'Use virtual environments, you guys',
    'author': 'Scott'
}
post_3 = {
    'title': 'Learning Python',
    'content': 'Learn Python, it is easy',
    'author': 'Bill'
}
# new_result = test.insert_many([post_1, post_2, post_3])
# print('Multiple posts: {0}'.format(new_result.inserted_ids))