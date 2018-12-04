# importing the required modules
# importing the required modules
import bottle
from bottle import route, run, template, response, error, request, view, static_file, get, post, app
from beaker.middleware import SessionMiddleware
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.discovery import build
import json
import httplib2

import sys
IP_ADDRESS = sys.argv[1]

import twitter
from newsapi import NewsApiClient
import unicodedata

import creatingGlobalDicts
from queryOperations import getDocIDsDict
from queryOperations import getDescription
from queryOperations import get_sorted_titles
from queryOperations import get_sorted_urls
from queryOperations import get_sorted_descriptions


word_to_wordID = creatingGlobalDicts.get_lexicon_DB()
wordID_to_docIDs = creatingGlobalDicts.get_invertedIndex_DB()
docID_to_pageRank = creatingGlobalDicts.get_pageRank_DB()
docID_to_url = creatingGlobalDicts.get_docIndex_DB()
docID_to_title = creatingGlobalDicts.get_titles_DB()
docID_to_description = creatingGlobalDicts.get_description_DB()


#if covariance is 0, gaussian rvs are independent


import requests

# from boto.manage.cmdhsell import sshclient_from_instance
#
# conn= boto.ec2.connect_to_region("us-east-1")
# resp = conn.run_instance("idonaws", instance_type="t2.micro", key_name="keypair" )

# reservations = conn.get_all_reservations()

import requests
from json import dumps
import imghdr

#library to implement leveinstein
from fuzzywuzzy import process

from collections import defaultdict
from pymongo import MongoClient
uri = "mongodb://zafeer:zafeer123@ds235785.mlab.com:35785/csc326_database"
client = MongoClient(uri, connectTimeoutMS=30000)

db = client.get_database("csc326_database")

#list to store all words of
choices = []

lexiconDB = db['Lexicon']
invertedIndexDB = db['Inverted_Index']
pageRankDB = db['Page_Rank']
docIndexDB = db['Doc_Index']

# the following is the dictionary that keeps a record of the top twenty words
topOccurences = dict()
userHistory = dict()
topOccurences = dict()
userHistory = dict()
docsSorted = list()

orderedDocIds = list()
titlesSorted = list()

descriptionsSorted = list()

results_per_page = 5
page = 1
firstWord = str()
pagesNeeded = 0
upperCount = 0
lowerCount = 0
listOfLists = list()
currentPage = 1
twitterUsers =[]
userTweets = []
newsArticlesHeadlines = []
newsArticlesImage = []
newsArticlesPublishedAt = []
newsArticlesDescription = []

searchMapString = ''
shouldSearchMap = False



session_opts = {
    'session.auto': True,
    'session.type': 'memory',
    'session.cookie_expires': 300  # sets how long should the user should stay logged in
}

userSignedIn = False
app = SessionMiddleware(bottle.app(), session_opts)
counter = 0


def finder(word = ""):
    print ('word:\t\t', word)
    word_id = 0

    wordPost = lexiconDB.find({'word': word})
    for post in wordPost:

        #Parse JSON object 'post' for the word_id
        word_id = post['word_id']
    print ('\nword_id:\t', word_id)
    if word_id == 0:
        return 0

    doc_IDs = list()
    docIDPost = invertedIndexDB.find({'word_id': word_id})
    for post in docIDPost:

        #Parse JSON object 'post' for the doc_IDs
        doc_IDs = post['doc_IDs']
    print ("\ndoc_IDs:\t",doc_IDs)

    pageRanks = {}
    for docID in doc_IDs:
        docIDPost = pageRankDB.find({'doc_id': docID})
        for post in docIDPost:

            #Parse JSON object 'post' for the url_ranks
            pageRank = post['url_ranks']
            pageRanks[docID] = pageRank
    print ("\npageRanks:\n",pageRanks)

    sortedRankingsList = sorted(pageRanks.items(), key=lambda x:-x[1])
    print ("\nsortedRankingsList:\n",sortedRankingsList)
    if len(sortedRankingsList) > 0:
        urlsInSortedPageRankOrder = list()
        for (docID, pageRank) in sortedRankingsList:
            urlPost = docIndexDB.find({'doc_id': docID})
            for post in urlPost:

                #Parse JSON object 'post' for the url
                url = post['url']
                urlsInSortedPageRankOrder.append(url)
        print ("\nUrls in sorted Page Rank order:\n",urlsInSortedPageRankOrder)
        return urlsInSortedPageRankOrder

    return len(sortedRankingsList)

#data for maps

search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
details_url = "https://maps.googleapis.com/maps/api/place/details/json"

@get('/maps')
def retreive():
    global shouldSearchMap
    global IP_ADDRESS
    shouldSearchMap = True
    print('/maps: ', shouldSearchMap)
    return template('layout.tpl', IP_ADDRESS=IP_ADDRESS)

@get("/sendRequest")
def results():
    global searchMapString

    global shouldSearchMap
    shouldSearchMap = True
    searchSentence = searchMapString
    print(searchSentence)
    search_payload = {"key":"AIzaSyAp4crTmwbO0APwD63f7kPFmewOTRdeo1Y", "query":str(searchSentence), 'location': '43.66001,-79.3948'}
    search_req = requests.get(search_url, params=search_payload)
    search_json = search_req.json()
    print(search_json)

    place_id = search_json["results"][0]["place_id"]

    details_payload = {"key":"AIzaSyAp4crTmwbO0APwD63f7kPFmewOTRdeo1Y", "placeid":place_id}
    details_resp = requests.get(details_url, params=details_payload)
    details_json = details_resp.json()

    url = details_json["result"]["url"]
    print('/sendRequest', shouldSearchMap)
    #url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query=starbucks&location=44.2666,-78.3745&radius=10000&key=AIzaSyAp4crTmwbO0APwD63f7kPFmewOTRdeo1Y'
    bottle.redirect(url)
    return dumps({'result' : details_json})


#retrieve twitter data

def getTweet(query):

    global userTweets
    global twitterUsers

    userTweets = list()
    twitterUsers = list()

    api = twitter.Api(consumer_key='M4qa2d6Cunkbe90qoSvEi9x1B',
      consumer_secret='a2NnfzUkoa2fjRzGmHe9NjAJmEXwhbyTd0Gg1QjypAUGPIpV1I',
      access_token_key='3703302855-lgDPmoN7kskZgtLLaYoTfh0ZdQAHk3Wrb2DIfCp',
      access_token_secret='8hs6jXXMm1VbFkOgcslzaMSTIebsdFhyfEujqMkG5XaUh')


    search = api.GetSearch(str(query))



    # print('name is ', str(search))
    for tweet in search:
        print(tweet)
        words = str(tweet)
        print(words)
        names = words.split('"screen_name": "')
        name = names[1].split('"')[0]
        userTweets.append(tweet.text)
        twitterUsers.append(name)



#retrieve news data

def newsArticles(topic):

    global newsArticlesHeadlines
    global newsArticlesImage
    global newsArticlesPublishedAt
    global newsArticlesDescription

    newsArticlesHeadlines = list()
    newsArticlesImage = list()
    newsArticlesPublishedAt = list()
    newsArticlesDescription = list()


    API_KEY = '165ff30e87b74f1daa7b82754e81541b'
    newsapi = NewsApiClient(api_key=API_KEY)
    headlines = newsapi.get_top_headlines(q=topic)



    articles = headlines["articles"]

    for article in articles:

        newsArticlesDescription.append(str(article['description']))
        newsArticlesHeadlines.append(str(article['title']))
        newsArticlesPublishedAt.append((str(article['publishedAt'])))
        newsArticlesImage.append((str(article['urlToImage'])))





# the get method loads the home page when the server starts  and then
# the html form called in object template, redirects to the post method
@get('/')
def getMethod():
    # using the global signed in variable here
    global userSignedIn
    global counter
    global shouldSearchMap
    global IP_ADDRESS

    shouldSearchMap = False


    if userSignedIn:
        counter += 1
        print(counter)
        bottle.redirect("http://" + IP_ADDRESS + "/login")

    # if user is already logged in
    return template("object", IP_ADDRESS=IP_ADDRESS)

# this method enables the counting of words in results
@post('/')
def index():
    global userSignedIn
    global docsSorted
    global firstWord
    global pagesNeeded
    global newsArticlesImage
    global newsArticlesPublishedAt
    global newsArticlesHeadlines
    global newsArticlesDescription

    global titlesSorted

    global descriptionsSorted
    global shouldSearchMap
    global searchMapString
    global IP_ADDRESS

    print('post /: ', shouldSearchMap)



    occurencesList = []
    sortedTopTwentyDictionary = dict()
    searchSentence = ""

    # getting the sentence entered by the user
    searchSentence = request.forms.get('search')
    print('search sentence is: ', searchSentence)

    # making sure not to pass in an empty string
    if (searchSentence != None):
        if shouldSearchMap:
            searchMapString = searchSentence
            print('Im here')
            bottle.redirect("http://" + IP_ADDRESS + "/sendRequest")
        searchSentence = searchSentence.lower()
        occurences = countNumberOfWords(searchSentence)

        # converting to list to arrange in descending order by value
        occurencesList = sorted(occurences.items(), key=lambda t: t[1], reverse=True)
        print(occurencesList)
    num = 1
    # passing essential details to the template to dsiplay on the front page
    picture_name = "logo_transparent.png"
    if (searchSentence != None):
        firstWord = searchSentence.lower().split()[0]

        orderedDocIds = getDocIDsDict(firstWord, word_to_wordID, wordID_to_docIDs, docID_to_pageRank)
        if len(orderedDocIds) == 0:
            bottle.redirect('http://" + IP_ADDRESS + "/urlNonExistent')
        titlesSorted = get_sorted_titles(orderedDocIds, docID_to_title, docID_to_url)
        docsSorted = get_sorted_urls(orderedDocIds, docID_to_url)

        descrByQuery = getDescription(firstWord, docID_to_description)
        descriptionsSorted = get_sorted_descriptions(orderedDocIds, descrByQuery)


        getTweet(firstWord)
        newsArticles(firstWord)
        docsSorted = finder(firstWord)
        if (docsSorted == 0):
            bottle.redirect("http://" + IP_ADDRESS + "/urlNonExistent")
        if len(docsSorted) <= 5:
            print('lenghthidouevbibev is ', len(newsArticlesHeadlines))
            return template('index', occurences=occurencesList, firstWord=firstWord, IP_ADDRESS=IP_ADDRESS,
                            picture=picture_name, searchSentence=searchSentence, urlsList=docsSorted, userTweets=userTweets,
                            twitterUsers=twitterUsers, newsArticlesHeadlines=newsArticlesHeadlines,
                            newsArticlesDescription=newsArticlesDescription, newsArticlesPublishedAt=newsArticlesPublishedAt,
                            newsArticlesImage=newsArticlesImage, descriptionList=descriptionsSorted, titlesList=titlesSorted)
        else:
            remainder = len(docsSorted) % 5
            print('remainder is: ', remainder)
            counter = 0
            if remainder == 0:
                pagesNeeded = len(docsSorted) / 5
                print('yahan hun')
                print(pagesNeeded)
            else:
                print('ithe')
                pagesNeeded = (len(docsSorted) // 5) + 1
                print(pagesNeeded)
            newURl = "http://" + IP_ADDRESS + "/results/1"
            bottle.redirect(newURl)

    if(docsSorted == 0):
        bottle.redirect("http://" + IP_ADDRESS + "/urlNonExistent")

    return template('index', IP_ADDRESS=IP_ADDRESS,
                    picture=picture_name, urlsList=docsSorted)

@get('/results/<pageNumber>')
def displayResults(pageNumber):

    global titlesSorted
    global docsSorted
    global descriptionsSorted

    global page
    global results_per_page
    global firstWord
    global userSignedIn

    global pagesNeeded
    global upperCount
    global lowerCount
    global currentPage
    global IP_ADDRESS
    listOfLists = list()

    getTweet(firstWord)
    print(twitterUsers)
    print(userTweets)

    currentPage = int(pageNumber)
    print("earlier current page number is: ", currentPage)

    if(docsSorted == 0):
        bottle.redirect("http://" + IP_ADDRESS + "/urlNonExistent")
    nextPage = 0
    previousPage = 0
    upperCount = 5
    lowerCount = 0
    newdocs = list()
    reip = 1

    listOfListsTitles = []
    listOfLists = []
    listOfListsDescriptions = []

    while reip <= pagesNeeded:
        newListTitles = titlesSorted[lowerCount:upperCount]
        newListDescriptions = descriptionsSorted[lowerCount:upperCount]

        newList = docsSorted[lowerCount:upperCount]
        #print('printing new list: ')
        #print(newList)
        listOfListsTitles.append(newListTitles)

        listOfListsDescriptions.append(newListDescriptions)

        listOfLists.append(newList)
        lowerCount = upperCount
        upperCount += 5
        reip += 1
    #print('list of lists')
    #print(listOfLists)
    #print(lowerCount)
    #print(upperCount)
    newTitles = listOfListsTitles[currentPage-1]
    print ("New Titles", newTitles)
    newdocs = listOfLists[currentPage-1]
    newDescriptions = listOfListsDescriptions[currentPage - 1]

    if currentPage == pagesNeeded:
        nextPage = pagesNeeded
        picture_name = "logo_transparent.png"
        #print('pages needed is: ', pagesNeeded)
        previousPage = currentPage - 1
        return template('noNextButton', previousPage=previousPage, firstWord = firstWord, IP_ADDRESS=IP_ADDRESS,
                        picture=picture_name, urlsList=newdocs, currentPage=currentPage, listOfLists=listOfLists,
                        pagesNeeded=pagesNeeded, titlesList=newTitles, userTweets=userTweets,
                        twitterUsers=twitterUsers, newsArticlesHeadlines=newsArticlesHeadlines,
                        newsArticlesDescription=newsArticlesDescription, newsArticlesPublishedAt=newsArticlesPublishedAt,
                        newsArticlesImage=newsArticlesImage, descriptionList=newDescriptions)





    if currentPage == 1:
        previousPage = 1
        nextPage = currentPage + 1
        picture_name = "logo_transparent.png"
        #print('pages needed is: ', pagesNeeded)
        return template('noPreviousButton', nextPage=nextPage, firstWord = firstWord, IP_ADDRESS=IP_ADDRESS,
                        picture=picture_name, urlsList=newdocs, currentPage=currentPage, listOfLists=listOfLists,
                        pagesNeeded=pagesNeeded, titlesList=newTitles, userTweets=userTweets,
                        twitterUsers=twitterUsers, newsArticlesHeadlines=newsArticlesHeadlines,
                        newsArticlesDescription=newsArticlesDescription, newsArticlesPublishedAt=newsArticlesPublishedAt,
                        newsArticlesImage=newsArticlesImage, descriptionList=newDescriptions)

    nextPage = currentPage + 1

    previousPage = currentPage - 1


    picture_name = "logo_transparent.png"
    #print('pages needed is: ', pagesNeeded)
    return template('newIndex', nextPage=nextPage, previousPage=previousPage, firstWord = firstWord, IP_ADDRESS=IP_ADDRESS,
                        picture=picture_name, urlsList=newdocs, currentPage=currentPage, listOfLists=listOfLists,
                        pagesNeeded=pagesNeeded, titlesList=newTitles, userTweets=userTweets,
                        twitterUsers=twitterUsers, newsArticlesHeadlines=newsArticlesHeadlines,
                        newsArticlesDescription=newsArticlesDescription, newsArticlesPublishedAt=newsArticlesPublishedAt,
                        newsArticlesImage=newsArticlesImage, descriptionList=newDescriptions)




#following oauth google documentation
@get('/login')
def login():
    global userSignedIn
    userSignedIn = True

    flow = flow_from_clientsecrets("client_secret.json",
                                   redirect_uri="http://" + IP_ADDRESS + "/redirect",
                                   scope='https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email'
                                   )
    uri = flow.step1_get_authorize_url()
    bottle.redirect(str(uri))

@get('/urlNonExistent')
def urlNonExistent():
    global IP_ADDRESS
    return template('error', IP_ADDRESS = IP_ADDRESS)

#user gets here when logged in
@get('/redirect')
def redirect_page():
    global userSignedIn

    if not userSignedIn:
        bottle.redirect("http://" + IP_ADDRESS + "/")
    code = request.query.get('code', '')


    with open('client_secret.json') as json_data:
        data = json.load(json_data)



    # following oauth documentation on google api
    code = request.query.get('code', '')
    client_id = data['web']['client_id']
    client_secret =  data['web']['client_secret']
    scope = 'https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email'

    flow = OAuth2WebServerFlow(client_id=client_id, client_secret=client_secret, scope=scope,
                               redirect_uri="http://" + IP_ADDRESS + "/redirect")
    credentials = flow.step2_exchange(code)
    token = credentials.id_token['sub']

    response.set_cookie("token", str(token))  # store token

    http = httplib2.Http()
    http = credentials.authorize(http)

    # Retrieving the user email
    userService = build('oauth2', 'v2', http=http)
    userDocument = userService.userinfo().get().execute()
    userEmail = userDocument['email']

    # saving the user's email
    response.set_cookie("email", str(userEmail))

    #template returns the display

    return template("loggedIn", user_email=userEmail)



@post('/redirect')
def displayResults():
    user_email = request.get_cookie("email")
    global userHistory
    global docsSorted
    global firstWord
    global pagesNeeded

    global newsArticlesImage
    global newsArticlesPublishedAt
    global newsArticlesHeadlines
    global newsArticlesDescription

    global titlesSorted

    global descriptionsSorted
    global shouldSearchMap
    global searchMapString



    # results table
    # getting the sentence entered by the user
    searchSentence = request.forms.get('search')

    # making sure not to pass in an empty string
    if (searchSentence != None):
        searchSentence = searchSentence.lower()
        occurences = countNumberOfWords(searchSentence)

        # converting to list to arrange in descending order by value
        occurencesList = sorted(occurences.items(), key=lambda t: t[1], reverse=True)
        print(occurencesList)

    # Top 20 searched words table
    s = bottle.request.environ.get('beaker.session')

    if user_email not in userHistory:  # create data for user if their email hasn't been used yet
        userHistory[user_email] = searchSentence + " "
    else:
        userHistory[user_email] += searchSentence + " "

    sentence = userHistory[user_email]
    # making sure not to pass in an empty string
    if (sentence != None):
        sentence = sentence.lower()
        newOccurences = countNumberOfWords(sentence)

        # obtaining the top twenty out of all the top occurences
        topTwenty = sorted(newOccurences.items(), key=lambda t: t[1], reverse=True)
        topTwenty = topTwenty[:20]

#passing essential details to the template to display on the front page
    picture_name = "logo_transparent.png"
    if (searchSentence != None):
        firstWord = searchSentence.lower().split()[0]
        orderedDocIds = getDocIDsDict(firstWord, word_to_wordID, wordID_to_docIDs, docID_to_pageRank)
        if len(orderedDocIds) == 0:
            bottle.redirect('http://" + IP_ADDRESS + "/urlNonExistent')
        titlesSorted = get_sorted_titles(orderedDocIds, docID_to_title, docID_to_url)
        docsSorted = get_sorted_urls(orderedDocIds, docID_to_url)

        descrByQuery = getDescription(firstWord, docID_to_description)
        descriptionsSorted = get_sorted_descriptions(orderedDocIds, descrByQuery)

        getTweet(firstWord)
        newsArticles(firstWord)
        docsSorted = finder(firstWord)
        if (docsSorted == 0):
            bottle.redirect("http://" + IP_ADDRESS + "/urlNonExistent")
        if len(docsSorted) <= 5:
            return template('loggedInResults',
                            picture=picture_name, searchSentence=searchSentence, urlsList=docsSorted, user_email=user_email,  userTweets=userTweets,
                            twitterUsers=twitterUsers, newsArticlesHeadlines=newsArticlesHeadlines,
                            newsArticlesDescription=newsArticlesDescription, newsArticlesPublishedAt=newsArticlesPublishedAt,
                            newsArticlesImage=newsArticlesImage, descriptionList=descriptionsSorted, titlesList=titlesSorted)
        else:
            remainder = len(docsSorted) % 5
            print('remainder is: ', remainder)
            counter = 0
            if remainder == 0:
                pagesNeeded = len(docsSorted) / 5
                print('yahan hun')
                print(pagesNeeded)
            else:
                print('ithe')
                pagesNeeded = (len(docsSorted) // 5) + 1
                print(pagesNeeded)
            newURl = "http://" + IP_ADDRESS + "/resultsLoggedIn/1"
            bottle.redirect(newURl)

    if(docsSorted == 0):
        bottle.redirect("http://" + IP_ADDRESS + "/urlNonExistent")


@get('/resultsLoggedIn/<pageNumber>')
def displayResults(pageNumber):
    user_email = request.get_cookie("email")
    global titlesSorted
    global docsSorted
    global descriptionsSorted

    global page
    global results_per_page
    global firstWord
    global userSignedIn

    global pagesNeeded
    global upperCount
    global lowerCount
    global currentPage
    listOfLists = list()

    getTweet(firstWord)
    print(twitterUsers)
    print(userTweets)

    currentPage = int(pageNumber)
    print("earlier current page number is: ", currentPage)

    if(docsSorted == 0):
        bottle.redirect("http://" + IP_ADDRESS + "/urlNonExistent")
    nextPage = 0
    previousPage = 0
    upperCount = 5
    lowerCount = 0
    newdocs = list()
    reip = 1

    listOfListsTitles = []
    listOfLists = []
    listOfListsDescriptions = []

    while reip <= pagesNeeded:
        newListTitles = titlesSorted[lowerCount:upperCount]
        newListDescriptions = descriptionsSorted[lowerCount:upperCount]

        newList = docsSorted[lowerCount:upperCount]
        #print('printing new list: ')
        #print(newList)
        listOfListsTitles.append(newListTitles)

        listOfListsDescriptions.append(newListDescriptions)

        listOfLists.append(newList)
        lowerCount = upperCount
        upperCount += 5
        reip += 1
    #print('list of lists')
    #print(listOfLists)
    #print(lowerCount)
    #print(upperCount)
    newTitles = listOfListsTitles[currentPage-1]
    print ("New Titles", newTitles)
    newdocs = listOfLists[currentPage-1]
    newDescriptions = listOfListsDescriptions[currentPage - 1]

    if currentPage == pagesNeeded:
        nextPage = pagesNeeded
        previousPage = currentPage - 1
        picture_name = "logo_transparent.png"
        print('pages needed is: ', pagesNeeded)
        return template('noNextButtonLoggedIn',previousPage=previousPage, firstWord = firstWord,
                        picture=picture_name, urlsList=newdocs, currentPage=currentPage, listOfLists=listOfLists,
                        pagesNeeded=pagesNeeded, titlesList=newTitles, userTweets=userTweets,
                        twitterUsers=twitterUsers, newsArticlesHeadlines=newsArticlesHeadlines,
                        newsArticlesDescription=newsArticlesDescription, newsArticlesPublishedAt=newsArticlesPublishedAt,
                        newsArticlesImage=newsArticlesImage, descriptionList=newDescriptions, user_email=user_email)





    if currentPage == 1:
        previousPage = 1
        nextPage = currentPage + 1
        picture_name = "logo_transparent.png"
        print('pages needed is: ', pagesNeeded)
        return template('noPreviousButtonLoggedIn', nextPage=nextPage, firstWord = firstWord,
                        picture=picture_name, urlsList=newdocs, currentPage=currentPage, listOfLists=listOfLists,
                        pagesNeeded=pagesNeeded, titlesList=newTitles, userTweets=userTweets,
                        twitterUsers=twitterUsers, newsArticlesHeadlines=newsArticlesHeadlines,
                        newsArticlesDescription=newsArticlesDescription, newsArticlesPublishedAt=newsArticlesPublishedAt,
                        newsArticlesImage=newsArticlesImage, descriptionList=newDescriptions, user_email=user_email)



    nextPage = currentPage + 1

    previousPage = currentPage - 1

    picture_name = "logo_transparent.png"
    print('pages needed is: ', pagesNeeded)
    return template('newLoggedInResults', nextPage=nextPage, previousPage=previousPage, firstWord = firstWord,
                        picture=picture_name, urlsList=newdocs, currentPage=currentPage, listOfLists=listOfLists,
                        pagesNeeded=pagesNeeded, titlesList=newTitles, userTweets=userTweets,
                        twitterUsers=twitterUsers, newsArticlesHeadlines=newsArticlesHeadlines,
                        newsArticlesDescription=newsArticlesDescription, newsArticlesPublishedAt=newsArticlesPublishedAt,
                        newsArticlesImage=newsArticlesImage, descriptionList=newDescriptions, user_email=user_email)




@error(404)
def error404(error):
    return template('error')

@error(500)
def error500(error):
    return template('error')

#defines the logout method
@get('/logout')
def logout():

    token = request.get("token")
    requests.post('https://accounts.google.com/o/oauth2/revoke', params={'token': token},
                  headers={'content-type': 'application/x-www-form-urlencoded'})

    global userSignedIn
    userSignedIn = False

    bottle.redirect("http://" + IP_ADDRESS + "/")

# enables search engine logo to be displayed
@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./views/myfiles')


# the function counts the number of words and appends them to the dictionary
# for result and history table
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


# starting the server
if __name__ == '__main__':

    #retreiving the database
    cursor = lexiconDB.find({})

    for document in cursor:
        choices.append(document['word'])
    global IP_ADDRESS
    run(host='0.0.0.0', port=80)
