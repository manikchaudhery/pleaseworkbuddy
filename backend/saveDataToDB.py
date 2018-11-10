from crawler import crawler

crawler = crawler(None, 'urls.txt')
crawler.crawl(depth=1)
crawler.lexicon_to_DB()
crawler.invertedIndex_to_DB()
crawler.page_rank_to_DB()
crawler.docIndex_to_DB()