# importing the required modules
import bottle
from bottle import route, run, template, response, request, view, static_file, get, post, app
from beaker.middleware import SessionMiddleware
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.discovery import build
import json
import httplib2
import requests

# the following is the dictionary that keeps a record of the top twenty words
topOccurences = dict()
userHistory = dict()

session_opts = {
    'session.auto': True,
    'session.type': 'memory',
    'session.cookie_expires': 300  # sets how long should the user should stay logged in
}

userSignedIn = False
app = SessionMiddleware(bottle.app(), session_opts)
counter = 0

# the get method loads the home page when the server starts  and then
# the html form called in object template, redirects to the post method
@get('/')
def getMethod():
    # using the global signed in variable here
    global userSignedIn
    global counter


    if userSignedIn:
        counter += 1
        print(counter)
        bottle.redirect("http://localhost:8080/login")

    # if user is already logged in
    userSignedIn = True
    return template("object")

# this method enables the counting of words in results
@post('/')
def index():
    global userSignedIn

    occurencesList = []
    sortedTopTwentyDictionary = dict()
    searchSentence = ""

    # getting the sentence entered by the user
    searchSentence = request.forms.get('search')

    # making sure not to pass in an empty string
    if (searchSentence != None):
        searchSentence = searchSentence.lower()
        occurences = countNumberOfWords(searchSentence)

        # converting to list to arrange in descending order by value
        occurencesList = sorted(occurences.items(), key=lambda t: t[1], reverse=True)
        print(occurencesList)

    # passing essential details to the template to dsiplay on the front page
    picture_name = "logo_transparent.png"

    return template('index', occurences=occurencesList,
                    picture=picture_name, searchSentence=searchSentence)


#following oauth google documentation
@get('/login')
def login():
    global userSignedIn
    userSignedIn = True

    flow = flow_from_clientsecrets("client_secret.json",
                                   redirect_uri="http://localhost:8080/redirect",
                                   scope='https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email'
                                   )
    uri = flow.step1_get_authorize_url()
    bottle.redirect(str(uri))

#user gets here when logged in
@get('/redirect')
def redirect_page():
    global userSignedIn

    if not userSignedIn:
        bottle.redirect("http://localhost:8080")
    code = request.query.get('code', '')


    with open('client_secret.json') as json_data:
        data = json.load(json_data)



    # following oauth documentation on google api
    code = request.query.get('code', '')
    client_id = data['web']['client_id']
    client_secret =  data['web']['client_secret']
    scope = 'https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email'

    flow = OAuth2WebServerFlow(client_id=client_id, client_secret=client_secret, scope=scope,
                               redirect_uri="http://localhost:8080/redirect")
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

#passing essential details to the template to dsiplay on the front page
    picture_name = "logo_transparent.png"
    return template('loggedInResults', occurences=occurencesList, sortedTopTwentyDictionary=topTwenty,
					picture=picture_name, searchSentence=searchSentence, user_email=user_email)



#defines the logout method
@get('/logout')
def logout():

    token = request.get("token")
    requests.post('https://accounts.google.com/o/oauth2/revoke', params={'token': token},
                  headers={'content-type': 'application/x-www-form-urlencoded'})

    global userSignedIn
    userSignedIn = False

    bottle.redirect("http://0.0.0.0:8080")

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
    run(host='0.0.0.0', port=80)
