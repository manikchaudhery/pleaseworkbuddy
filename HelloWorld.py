from bottle import route, run, template, Response, request, view

topOccurences = dict()


@route('/')
def index():
    return template('index')


@route('/', method='POST')
#@view('object.tpl')
def doCounting():
    searchSentence = request.forms.get('search')

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

    result = sorted(topOccurences.items(), key=lambda t: t[1], reverse=True)
    print("printing result now")
    for k, v in result:
        print(k, v)
    print("occurences in funcion are ", occurences)
    return occurences


@route('/querytest')
def querytest():
    param1 = request.query.param1
    param2 = request.query.param2


if __name__ == '__main__':
    run(host='localhost', port=8080, debug=False, reloader=True)

'''
<!DOCTYPE=HTML>
        <form action="/login" method="post">
           <input name="Search" type="text" />

            <input value="Search" type="submit" />
        </form>

@route('/', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(username, password):
        return "<p>Your login information was correct.</p>"
    else:
        return "<p>Login failed.</p>"
run(host='localhost', port=9090, debug=True)
'''
