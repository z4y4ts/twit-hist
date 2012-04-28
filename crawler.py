#!/usr/bin/env python

from urllib import urlencode, urlopen
import json
import urllib
import pprint

from pymongo import Connection


def fetch_tweets(htags):
    base_url = 'http://search.twitter.com/search.json?q='
    # url = 'http://search.twitter.com/search.json?q=%40douhack'
    for htag in htags:
        url = base_url + urllib.quote(htag)
        print 'fetching ', url
        d = json.loads(urlopen(url).read())
        raw_tweets = d['results']
        next_page = d.get('next_page', None)
        while next_page:
            url = urllib.basejoin(base_url, next_page)
            print 'fetching ', url
            d = json.loads(urlopen(url).read())
            raw_tweets += d['results']
            next_page = d.get('next_page', None)
        return raw_tweets


def save_tweet(htag, tweet):
    conn = Connection()
    db = conn.twit
    tweet_data = {'hashes': [htag], 'data': json.dumps(tweet)}
    db.tweet.insert(tweet_data)


def main():
    tags = ['#douhack', '#uwcua']
    tags = ['#douhack']
    tweets = fetch_tweets(tags)
    # for tweet in tweets:
    #     save_tweet(tweet)


if __name__ == '__main__':
    main()
