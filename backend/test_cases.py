#Testing the correctness of the crawler

from crawler import crawler

def test_inverted_index(crawler):
    print "1) Testing the inverted index..."

    inverted_index = crawler.get_inverted_index()

    #Checking if the inverted index contains all the wordIDs
    wordID_check = True
    for word in crawler._word_id_cache:
	word_id = crawler._word_id_cache[word]
	if word_id not in inverted_index:
	    print "Word: ", word, " is not in the inverted_index"
	    wordID_check = False

    if not wordID_check:
	return False

    
    #Checking if the inverted index contains valid documentIDs
    docID_check = True
    for wordID, docIDs in inverted_index.items():
	for docID in docIDs:
	    if docID not in crawler._doc_id_cache.values():
	        print "DocID: ", docID, " is not in the _doc_id_cache"
	        docID_check = False

    if not docID_check:
	return False

    return True

def test_res_inverted_index(crawler):
    print "2) Testing the resolved inverted index..."
    
    res_inverted_index = crawler.get_resolved_inverted_index()

    #Checking if the resolved inverted index contains all the words
    word_check = True
    for word in crawler._word_id_cache:
	if word not in res_inverted_index:
	    print "Word: ", word, " is not in the inverted_index"
	    word_check = False

    if not word_check:
	return False

    #Checking if the resolved inverted index contains valid urls
    url_check = True
    for word, urls in res_inverted_index.items():
	for url in urls:
	    if url not in crawler._doc_id_cache:
	        print "URL: ", url, " is not in the _doc_id_cache"
	        url_check = False

    if not url_check:
	return False
    
    return True

def test_invIndex_equals_resInvIndex(crawler):
    print "3) Testing to see if the inverted index correlates with the resolved inverted index..."
    
    inverted_index = crawler.get_inverted_index()
    res_inverted_index = crawler.get_resolved_inverted_index()

    word_wordID_check = True
    url_docID_check = True

    for word, urls in res_inverted_index.items():
	word_id = crawler._word_id_cache[word]
	
	#Check if each word in the resolved inverted index corresponds with the wordID in the inverted index
	if word_id not in inverted_index:
	    print "Word: ", word, " is not linked"
	    word_wordID_check = False
	
	inv_indx_docIDs = inverted_index[word_id]
	for url in urls:
	    docID = crawler._doc_id_cache[url]
	    
	    #Check if each URL in the resolved inverted index corresponds with the correct documentID in the inverted index
	    if docID not in inv_indx_docIDs:
		print "URL: ", url, " is not linked"
		url_docID_check = False

    if not word_wordID_check or not url_docID_check:
	return False
    
    return True

bot = crawler(None, "urls.txt")
bot.crawl(depth=0)

print "\n\n***Testing the correctness of the crawler***\n"

if test_inverted_index(bot):
    print "\tPASS --- The wordIDs and documentIDs in the inverted_index are valid\n"
else:
    print "\tFAIL --- The wordIDs and/or documentIDs in the inverted_index are NOT valid\n"

if test_res_inverted_index(bot):
    print "\tPASS --- The words and urls in the resolved_inverted_index are valid\n"
else:
    print "\tFAIL --- The words and/or urls in the resolved_inverted_index are NOT valid\n"

if test_invIndex_equals_resInvIndex(bot):
    print "\tPASS --- The inverted_index correlates to the resolved inverted index\n"
else:
    print "\tFAIL --- The inverted_index DOES NOT correlate to the resolved inverted index\n"

print "***Done Testing the correctness of the crawler***\n"

 
