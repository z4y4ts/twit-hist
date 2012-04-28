#!/usr/bin/env python

import json
import sys
import urllib
from datetime import datetime, time

from pymongo import Connection

# import data


class Crawler(object):
    def __init__(self):
        self.conn = Connection()
        self.db = self.conn.twit

    def to_datetime(self, string):
        time_format = '%a, %d %b %Y %H:%M:%S +0000'
        t = time.strptime(string, time_format)
        return datetime(
                year=t.tm_year,
                month=t.tm_mon,
                day=t.tm_mday,
                hour=t.tm_hour,
                minute=t.tm_min,
                second=t.tm_sec)

    def fetch_tweets(self, htags):
        base_url = 'http://search.twitter.com/search.json?q='
        res = {}
        for htag in htags:
            url = base_url + urllib.quote(htag)
            print('fetching ', url)
            d = json.loads(urllib.urlopen(url).read())
            raw_tweets = d['results']
            next_page = d.get('next_page', None)
            while next_page:
                url = urllib.basejoin(base_url, next_page)
                print('fetching ', url)
                d = json.loads(urllib.urlopen(url).read())
                raw_tweets += d['results']
                next_page = d.get('next_page', None)
                # next_page = None
            res[htag] = raw_tweets
        return res

    def save_tweet(self, htag, tweet):
        try:
            tweet_data = {'htags': [htag],
                          'id': tweet['id'],
                          'datetime': self.to_datetime(tweet['created_at']),
                          'from_user': tweet['from_user'],
                          'profile_image_url': tweet['profile_image_url'],
                          'text': tweet['text']}
            db_tweet = self.db.tweet.find_one({'id': tweet_data['id']})
            if db_tweet:
                tweet_data['htags'] = list(set(db_tweet['htags']
                                               + tweet_data['htags']))
                self.db.tweet.update({'id': tweet_data['id']}, tweet_data)
            self.db.tweet.insert(tweet_data)
        except:
            pass

    def find_tweets(self, htag, date_from, date_to):
        conn = Connection()
        db = conn.twit
        dt_from = {'datetime': {'$gte': date_from}}
        dt_to = {'datetime': {'$lte': date_to}}
        query = {'htags': htag,
                 '$and': [dt_from, dt_to]}
        tweets = db.tweet.find(query)
        return (_ for _ in tweets)


def main(tags=[]):
    crawler = Crawler()
    tweets = crawler.fetch_tweets(tags)
    for htag, tweets in tweets.items():
        for tweet in tweets:
            crawler.save_tweet(htag, tweet)

if __name__ == '__main__':
    main(sys.argv[1:])
