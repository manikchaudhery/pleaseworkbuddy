#RETRIEVES DESCRIPTIONS RELATED TO QUERY
def getDescription(query, descriptions):
	search = query
	search = search.lower()

	finalDesc = {}
	#print descriptions

	for doc_id in descriptions:
		realText = descriptions[doc_id]
		text = descriptions[doc_id].lower()
		if search in text:
			realLines = realText.split(' | ')
			lines = text.split(' | ')
			num = 0
			for line in lines:
				if search in line:
					if doc_id in finalDesc:
						finalDesc[doc_id].append(realLines[num])
					else:
						finalDesc[doc_id] = [realLines[num]]
				num += 1

	if not finalDesc:
		print ("No description found")
	else:
		return finalDesc

#GET SORTED DOC_IDS IN PAGE RANK ORDER
def getDocIDsDict(query, word_to_wordID, wordID_to_docIDs, docID_to_pageRank):
	word = query
	word_id = word_to_wordID[word]
	doc_IDs = wordID_to_docIDs[word_id]

	pageRanks = {}
	for docID in doc_IDs:
		url_rank = docID_to_pageRank[docID]
		pageRanks[docID] = url_rank

	sortedRankingsList = sorted(pageRanks.items(), key=lambda x:-x[1])

	docIDsInSortedPageRankOrder = []
	for (docID, pageRank) in sortedRankingsList:
		docIDsInSortedPageRankOrder.append(docID)
	return docIDsInSortedPageRankOrder

def get_sorted_titles(orderedDocIds, docID_to_title, docID_to_url):
	titlesSorted = list()
	for docID in orderedDocIds:
		if docID in docID_to_title:
			titlesSorted.append(docID_to_title[docID])
		else:
			parsedURL = parseURL(str(docID_to_url[docID]))
			titlesSorted.append(parsedURL)

	return titlesSorted

def get_sorted_urls(orderedDocIds, docID_to_url):
	urlsSorted = list()

	for docID in orderedDocIds:
		urlsSorted.append(docID_to_url[docID])

	return urlsSorted

def get_sorted_descriptions(orderedDocIds, descrByQuery):
	descriptionsSorted = list()

	for docID in orderedDocIds:
		if docID != None:
			if docID in descrByQuery:
				count = 1
				for descLine in descrByQuery[docID]:
					descriptionsSorted.append(descLine)
					count += 1
			else:
				descriptionsSorted.append("No Description Available")

	return descriptionsSorted

def parseURL(url):
	words = []
	if "www." in url:
		words = url.split("www.")
	else:
		words = url.split("//")

	parsed = words[1].split(".")
	return parsed[0].capitalize()