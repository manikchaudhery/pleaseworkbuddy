from bottle import route, run, template, Response, request, view, static_file, get, post

import operator
from collections import OrderedDict

#the following is the dictionary that keeps a record of the top twenty words
topOccurences = dict()

#the get method loads the home page when the server starts  and then  
#the html form called in object template, redirects to the post method
@get('/')
def getMethod():
    return template('object')

#this method enables the counting of words in results and history
@post('/')
def index():

    occurencesList = []
    sortedTopTwentyDictionary = dict()
    searchSentence = ""

#getting the sentence entered by the user
    searchSentence = request.forms.get('search')

#making sure not to pass in an empty string
    if(searchSentence != None ):
        searchSentence = searchSentence.lower()
        occurences = countNumberOfWords(searchSentence)

#converting to list to arrange in descending order by value
        occurencesList = sorted(occurences.items(), key=lambda t:t[1], reverse=True)
        print (occurencesList)

#obtaining the top twenty out of all the top occurences 
        topTwenty = sorted(topOccurences.items(), key=lambda t:t[1], reverse=True)
        topTwenty = topTwenty[:20]


#passing essential details to the template to dsiplay on the front page
    picture_name = "logo_transparent.png"
    return template('index', occurences=occurencesList, sortedTopTwentyDictionary=topTwenty, 
					picture=picture_name, searchSentence=searchSentence)

#enables search engine logo to be displayed
@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./views/myfiles')

#the function counts the number of words and appends them to the dictionary
#for result and history table
def countNumberOfWords(sentence):
    wordsArray = sentence.split()
    occurences = dict()

    for word in wordsArray:
        if word not in occurences:
            occurences[word] = 1
        else:
            occurences[word] += 1

        if word not in topOccurences:
            topOccurences[word] = 1
        else:
            topOccurences[word] += 1


    print("occurences in funcion are ", occurences)
    return occurences


#starting the server
if __name__ == '__main__':
    run(host='localhost', port=8080, debug=False, reloader=True)
