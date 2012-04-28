#!/usr/bin/env python

import json
import urllib
from datetime import datetime

from pymongo import Connection
import protection

import data


def to_datetime(string):
    return protection.str2date(string, '%a, %d %b %Y %H:%M:%S +0000')


def fetch_tweets(htags):
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


def save_tweet(htag, tweet):
    conn = Connection()
    db = conn.twit
    try:
        tweet_data = {'htags': [htag],
                  'id': tweet['id'],
                  'datetime': to_datetime(tweet['created_at']),
                  'text': tweet['text']}
    except:
        pass
    try:
        if not db.tweet.find_one({'id': tweet['id']}):
            db.tweet.insert(tweet_data)
    except:
        pass


def find_tweets(htag, date_from, date_to):
    conn = Connection()
    db = conn.twit
    dt_from = {'datetime': {'$gte': date_from}}
    dt_to = {'datetime': {'$lte': date_to}}
    query = {'htags': htag,
             '$and': [dt_from, dt_to]}
    tweets = db.tweet.find(query)
    return (_ for _ in tweets)


def main():
    tags = ['#garage48']
    # tags = ['#douhack']
    tweets = fetch_tweets(tags)
    for tweet in tweets:
        # print tweet
        save_tweet('#douhack', tweet)


if __name__ == '__main__':
    main()
