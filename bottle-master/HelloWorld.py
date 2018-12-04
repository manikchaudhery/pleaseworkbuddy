# importing the required modules
import bottle
from bottle import route, run, template, response, request, view, static_file, get, post, app, error
from beaker.middleware import SessionMiddleware
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.discovery import build
import json
import httplib2
from paginator import finder
import requests

# the following is the dictionary that keeps a record of the top twenty words
from trash import getResults

topOccurences = dict()
userHistory = dict()
docsSorted = list()
results_per_page = 5
page = 1
firstWord = str()

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
    return template("object")

# this method enables the counting of words in results
@post('/')
def index():
    global userSignedIn
    global docsSorted
    global firstWord
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
    if (searchSentence != None):
        firstWord = searchSentence.lower().split()[0]
        docsSorted = finder(firstWord)
        bottle.redirect("http://localhost:8080/results")

    if(docsSorted == 0):
        bottle.redirect("http://localhost:8080/urlNonExistent")

    return template('index', occurences=occurencesList,
                    picture=picture_name, searchSentence=searchSentence, urlsList=number)


@get('/urlNonExistent')
def urlNonExistent():
    return template('error')
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
        bottle.redirect("http://localhost:8080/")
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

    bottle.redirect("http://localhost:8080/")

# enables search engine logo to be displayed
@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./views/myfiles')

@error(404)
def error404(error):
    return template('error')


@get('/results')
def displayResults():
    global docsSorted
    global page
    global results_per_page
    global firstWord
    global userSignedIn

    output = '''
<html>
<head>
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
	<style>	
	body {
		background-image: linear-gradient(to top, #f4fdff, white);
		background-repeat: no-repeat;
		height: 100%;
		overflow: hidden;
		}

	.main {
		position: absolute;
		top: 45%;
		left: 50%;
		transform: translate(-50%, -50%);
		}

	.search-box {
		height: 30px;
		border-radius: 40px;
		padding: 10px;
		border-style: solid;
		border-color: #72e7ff;
		background: white;
		transition: 0.4s;
		float: left;
		width: 20%;
		padding-left: 1%;
		}

	.search-box:hover, .search-box:focus-within {
		background: #72e7ff;
		box-shadow: none;
		border-color: white;
		box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.2), 0 2px 5px 0 rgba(0, 0, 0, 0.19);
		}

	.search-txt {
		border: none;
		background: none;
		outline: none;
		float: left;
		text-align: left;
		padding: 0;
		color: #036c82;
		font-size: 20px;
		line-height: 40px;
		width: 800px;
		}

	#submit {
		height: 50px;
		width: 60px;
		border: none;
		background: white;
		transition: 0.4s;
		border-radius: 40px;
		line-height: 30px;
		font-size: 16px;
		margin-left: 10px;
		margin-top: 0.2%;
		}

	#submit:hover {
		background: #72e7ff;
		border-color: #72e7ff;
		border-style: solid;
		border-width: 5px;
		box-shadow: none;
		box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.2), 0 2px 5px 0 rgba(0, 0, 0, 0.19);
		border-color: white;
		border-width: 3px;
		}

	.nav {
		background: #72e7ff;
		width: 100%;
		height: 8%;
		padding: 0;
		box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.2), 0 2px 5px 0 rgba(0, 0, 0, 0.19);
		padding-top: 0.5%;
		padding-right: 0.5%;
		padding-left: 0.2%;
		}

	#login {
		border: none;
		background: white;
		transition: 0.4s;
		border-radius: 40px;
		height: 50px;
		width: 150px;
		line-height: 30px;
		font-size: 16px;
		float: right;
		}

	#login:hover {
		border-color: white;
		border-style: solid;
		border-width: 3px;
		background: #72e7ff;
		color: white;
		font-weight: bold;
		box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.2), 0 2px 5px 0 rgba(0, 0, 0, 0.19);
		}

	#toptext {
		float: right;
		font-family: Trebuchet MS;
		margin-right: 1%;
		color: #036c82;
		font-style: italic;

		}
	#title {
		color: #036c82;
		font-family: Trebuchet MS;
		font-size: 48px;
		}

	.results {
		text-align: left;
		border-color: #036c82;
		border-style: solid;
		border-width: 3px;
		font-size: 20px;
		font-family: Trebuchet MS;
		background-color: white;
		box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
		}

	ul {
		padding-bottom: 20px;
		color: #036c82;
		}

	.pages {
		position: absolute;
		top: 85%;
		left: 50%;
		transform: translate(-50%, -50%);
		}

	#prev, #next {
		height: 50px;
		width: 60px;
		border: none;
		background: white;
		transition: 0.4s;
		border-radius: 40px;
		line-height: 30px;
		font-size: 16px;
		margin-left: 10px;
		margin-top: 0.2%;
		box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.2), 0 3px 10px 0 rgba(0, 0, 0, 0.19);
		font-weight: bold;
		}

	#prev:hover, #next:hover {
		background: #72e7ff;
		border-color: #72e7ff;
		border-style: solid;
		border-width: 5px;
		box-shadow: none;
		border-color: white;
		border-width: 3px;
		}

    </style>
</head>
<body>
	<section id="hero">
	<div class="nav">
		<form id="form" method="post">
			<div class="search-box">
				<input name="keywords" id="keywords" type="text" placeholder="Search..." class="search-txt"/>
			</div>
			<input name="search" id="submit" type="submit" class="btn" value="Go"></input>'''

    if userSignedIn:
        output += '''<a href="http://localhost:8080/logout"><button id="login" type="button" class="btn">Log Out</button></a><h2 id="toptext">''' + str(
            request.get_cookie("email")) + '''</h2>'''
    else:
        output += '''<a href="http://localhost:8080/login"><button id="login" type="button" class="btn">Log In</button></a>'''

    output += '''</form></div><div class="main"><h2 id="title">Results for "''' + firstWord + '''":</h2>''';

    if len(docsSorted) == 0:
        output += '''<div class="results"><ul>No results found.</ul></div>'''
    elif len(docsSorted) > results_per_page:
        output += multiPage(docsSorted, page, results_per_page)
    else:
        output += singlePage(docsSorted)
    return output


# use post to increment page, display different stuff depending on page
def multiPage(docList, page=1, results_per_page=5):
    output = '''<div class="results">''';

    # for i in range(len(docList) / 1):
    # output += "<input name='pg" + str(i) + "' type='submit' value='" + str(i) + "class='btn'></input>"

    for i in range(results_per_page):
        output += "<ul><a href='" + docList[i + results_per_page * (page - 1)][0] + "'>" + \
                  docList[i + results_per_page * (page - 1)][0] + "</a></ul>"

    output += '''
        </div>
	</div>
	<div class="pages">
	<form id="switchPage" method="post">'''

    if page > 1:  # i.e.: not on the first page
        output += '''<input name="prev" id="prev" type="submit" value="<<" class="btn"></input>'''

    if page * results_per_page < len(docList):  # i.e.: not on last page
        output += '''<input name="next" id="next" type="submit" value=">>" class="btn"></input>'''

    output += '''</form></div></section><body></html>'''

    return output


def singlePage(docList):
    output = '''<div class="results">'''

    for i in range(len(docList)):
        output += "<ul><a href='" + docList[i][0] + "'>" + docList[i][0] + "</a></ul>"

    output += '''</div></div></section><body></html>'''

    return output


@post('/results')
def changePage():
    global page

    if request.POST.get('next'):
        page += 1
    elif request.POST.get('prev'):
        page -= 1
    else:
        return getResults()

    return displayResults()


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
    run(host='localhost', port=8080, debug=True)