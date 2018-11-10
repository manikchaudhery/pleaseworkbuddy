from crawler import crawler
import pprint


crawler = crawler(None, 'urls.txt')
crawler.crawl(depth=1)
rankings = crawler.get_page_rank()
sortedRankingsList = sorted(rankings.iteritems(), key=lambda x:-x[1])
sortedRankingsDict = dict(sortedRankingsList)

# print "\nPage Ranks Pretty Print:"
# pprint.pprint(dict(rankings))

print "\nDoc_ID => URL_Rank"
pprint.pprint(sortedRankingsList)
