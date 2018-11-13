from collections import defaultdict
from pymongo import MongoClient
uri = "mongodb://zafeer:zafeer123@ds235785.mlab.com:35785/csc326_database"
client = MongoClient(uri, connectTimeoutMS=30000)

db = client.get_database("csc326_database")
docIDs = list()

lexiconDB = db['Lexicon']
invertedIndexDB = db['Inverted_Index']
pageRankDB = db['Page_Rank']
docIndexDB = db['Doc_Index']
def finder(word = ""):
    print ('word:\t\t', word)
    word_id = 0

    wordPost = lexiconDB.find({'word': word})
    for post in wordPost:

        #Parse JSON object 'post' for the word_id
        word_id = post['word_id']
    print ('\nword_id:\t', word_id)

    global doc_IDs
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

