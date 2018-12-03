from collections import defaultdict
from pymongo import MongoClient
#SETUP
uri = "mongodb://zafeer:zafeer123@ds235785.mlab.com:35785/csc326_database"
client = MongoClient(uri, connectTimeoutMS=30000)
db = client.get_database("csc326_database")

lexiconDB = db['Lexicon']
invertedIndexDB = db['Inverted_Index']
pageRankDB = db['Page_Rank']
docIndexDB = db['Doc_Index']
titlesDB = db['Titles']
descriptionDB = db['Descriptions']

#CREATING GLOBAL DICTIONARY OF LEXICON
def get_lexicon_DB():
	lexiconDict = {}
	words = lexiconDB.find({})
	for wordJSON in words:
		word_id = wordJSON['word_id']
		word = str(wordJSON['word'])

		lexiconDict[word] = word_id

	return lexiconDict

#CREATING GLOBAL DICTIONARY OF INVERTED INDEX
def get_invertedIndex_DB():
	invIdxDict = {}
	entries = invertedIndexDB.find({})
	for entryJSON in entries:
		word_id = entryJSON['word_id']
		doc_IDs = entryJSON['doc_IDs']

		invIdxDict[word_id] = doc_IDs
	return invIdxDict

#CREATING GLOBAL DICTIONARY OF pAGE RANKS
def get_pageRank_DB():
	pageRankDict = {}
	entries = pageRankDB.find({})
	for entryJSON in entries:
		doc_id = entryJSON['doc_id']
		url_rank = entryJSON['url_ranks']

		pageRankDict[doc_id] = url_rank
	return pageRankDict

#CREATING GLOBAL DICTIONARY OF DocIndex
def get_docIndex_DB():
	urlDict = {}
	urls = docIndexDB.find({})
	for urlJSON in urls:
		doc_id = urlJSON['doc_id']
		url = str(urlJSON['url'])

		urlDict[doc_id] = url
	return urlDict

#CREATING GLOBAL DICTIONARY OF TITLES 
def get_titles_DB():
	titleDict = {}
	titles = titlesDB.find({})
	for titleJSON in titles:
		doc_id = titleJSON['doc_id']
		title = str(titleJSON['title'])

		titleDict[doc_id] = title
	return titleDict

#CREATING GLOBAL DICTIONARY OF DESCTIPTIONS 
def get_description_DB():
	descrDict = {}
	descriptions = descriptionDB.find({})
	for descriptionJSON in descriptions:
		doc_id = descriptionJSON['doc_id']
		description = str(descriptionJSON['description'])

		descrDict[doc_id] = description
	return descrDict
