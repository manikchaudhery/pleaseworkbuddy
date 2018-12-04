from collections import defaultdict
from pymongo import MongoClient
uri = "mongodb://zafeer:zafeer123@ds235785.mlab.com:35785/csc326_database"
client = MongoClient(uri, connectTimeoutMS=30000)

db = client.get_database("csc326_database")
lexiconDB = db['Lexicon']

import autocorrect
from autocorrect import spell


def spell_check():
    ('HTe')
    # Retrieve all words in database
    keyword = 'enginee'
    word_list = []
    for i in range(2, 8):
        wordPost = lexiconDB.find({'word_id': i})
        word = ''
        for post in wordPost:
            word=post['word']
        word_list.append(word)

    print(word_list)


    #Calculate Levenshtein Distance
    closest_word = ''
    closest_dist = 100  # Make this infinity

    for word in word_list:
        # Make a (keyword x word) array
        row = [0] * len(word)     # Each row has "word" columns
        min_dist = row * len(keyword)   # There are "keyword" rows

        for row in range(len(keyword)):
            for col in range(len(word)):
                # Base Case
                if min(row, col) is 0:
                    min_dist[row][col] = int(max(row, col))
                # Sub-problem Optimization
                else:
                    min_dist[row][col] = min(min_dist[row-1][col] + 1, min_dist[row][col-1] + 1,
                                             min_dist[row-1][col-1] + (1 if keyword[row] == word[col] else 0))

        # Update closest word
        if min_dist[len(word) - 1][len(keyword) - 1] < closest_dist:
            closest_dist = min_dist[len(word) - 1][len(keyword) - 1]
            closest_word = word

    return closest_word

print(spell_check())