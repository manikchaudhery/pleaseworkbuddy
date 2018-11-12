print("here")
user_email = request.get_cookie("email")
output = '''<h3>''' + user_email + '''</h3><br><a href="http://localhost:8080/logout"><button id="logout" type="button" class="btn">Log Out</button></a>'''
global userHistory

# results table
userInput = request.forms.get('search')
words = userInput.split()
dictionary = dict()

# count number of times each word was entered
for x in words:
    if x in dictionary:
        dictionary[x] += 1
    else:
        dictionary[x] = 1

# create results table
output += "<h2>Search Results</h2><table name=\"results\"><tr><th>Word</th><th>Count</th><tr>"

# add a row to the results table for each word the user has entered
for key, value in dictionary.items():
    output += "<tr><td>" + key + "</td><td> &nbsp;&nbsp;&nbsp;&nbsp;" + str(value) + "</td></tr>"

output += "</table>"

# top 20 keywords table
s = bottle.request.environ.get('beaker.session')

if user_email not in userHistory:  # create data for user if their email hasn't been used yet
    userHistory[user_email] = userInput + " "
else:
    userHistory[user_email] += userInput + " "

keywords = userHistory[user_email]

keywords_split = keywords.split()
keywordsFreqs = dict()

for x in keywords_split:
    if x in keywordsFreqs:
        keywordsFreqs[x] += 1
    else:
        keywordsFreqs[x] = 1

# create history table
output += "<br><br><h2>Most Popular Keywords</h2><table name=\"history\"><tr><th>Word</th><th>Count</th><tr>"

# add a row to the history table for each word stored
counter = 0

for i in range(20):
    if i > (len(keywordsFreqs) - 1):
        break

    maxIndex = str()
    maxVal = 0

    for key, value in keywordsFreqs.items():
        if value > maxVal:
            maxIndex = key
            maxVal = value

    keywordsFreqs[maxIndex] = 0
    output += "<tr><td>" + maxIndex + "</td><td> &nbsp;&nbsp;&nbsp;&nbsp;" + str(maxVal) + "</td></tr>"

output += "</table>"

return output
