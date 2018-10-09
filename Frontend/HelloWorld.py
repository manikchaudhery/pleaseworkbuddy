from bottle import route, run, template, Response, request, view, static_file
import operator
from collections import OrderedDict

topOccurences = dict()


@route('/', method="POST")
def index():

    occurences = dict()
    sortedTopTwentyDictionary = dict()
    searchSentence = ""

    searchSentence = request.forms.get('search')
    if(searchSentence != None ):
        searchSentence = searchSentence.lower()
        occurences = countNumberOfWords(searchSentence)
        print (occurences)

        topTwenty = sorted(topOccurences.items(), key=lambda t:t[1], reverse=True)


        print("top twenty is: ", topTwenty)
        sortedTopTwentyDictionary = dict((topTwenty)[:20])
        print("printing dictionary", sortedTopTwentyDictionary)
    picture_name = "logo_transparent.png"
    return template('index', occurences=occurences, sortedTopTwentyDictionary=sortedTopTwentyDictionary, picture=picture_name)

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./views/myfiles')



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

def displayTopTwenty():


    topTwenty = sorted(topOccurences.items(), key=lambda t:t[1], reverse=True)


    print("top twenty is: ", topTwenty)
    sortedTopTwentyDictionary = dict((topTwenty)[:20])
    print("printing dictionary", sortedTopTwentyDictionary)
    picture_name = "logo_transparent.png"
    return template('index', sortedTopTwentyDictionary=sortedTopTwentyDictionary, picture=picture_name)



if __name__ == '__main__':
    run(host='localhost', port=8080, debug=False, reloader=True)

'''
from bottle import route, run, template, Response, request, view
import operator
from collections import OrderedDict

topOccurences = dict()


@route('/')
def index():
    return displayTopTwenty()



@route('/', method='POST')
def doCounting():
    searchSentence = request.forms.get('search')
    searchSentence = searchSentence.lower()
    occurences = countNumberOfWords(searchSentence)
    print (occurences)
    return template('object', occurences=occurences)


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

def displayTopTwenty():


    topTwenty = sorted(topOccurences.items(), key=lambda t:t[1], reverse=True)


    print("top twenty is: ", topTwenty)
    sortedTopTwentyDictionary = dict((topTwenty)[:20])
    print("printing dictionary", sortedTopTwentyDictionary)
    return template('index', sortedTopTwentyDictionary=sortedTopTwentyDictionary)



if __name__ == '__main__':
    run(host='localhost', port=8080, debug=False, reloader=True)

'''
