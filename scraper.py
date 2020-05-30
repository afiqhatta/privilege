from twitterscraper import query_tweets
import datetime as dt


class Scraper(object):

    def __init__(self, keyword, qty, start):
        self.keyword = keyword
        self.qty = qty
        self.start = start

    def get_batch(self):
        return query_tweets(self.keyword, limit=1, begindate=self.start, lang='en')[:self.qty]

    def get_text(self):
        return [item.text for item in self.get_batch()]

