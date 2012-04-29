from datetime import datetime
import os
import os.path
import tornado.ioloop
import tornado.web
import json
import crawler


class MainHandler(tornado.web.RequestHandler):
    def get(self, htag):
        c = crawler.Crawler()
        tweets = c.find_tweets(htag, datetime(2000, 1, 1), datetime(2100, 1, 1))
        if tweets:
            self.write(json.dumps({'htag': htag, 'count': len(tweets), 'results': list(tweets)}))
        else:
            c.crawl_tweets([htag])
            tweets = c.find_tweets(htag, datetime(2000, 1, 1), datetime(2100, 1, 1))
            self.write(json.dumps({'htag': htag, 'count': len(tweets), 'results': list(tweets)}))


class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html', **{'htag': '#douhack'})



settings = {
    'template_path': os.path.join(os.path.dirname(__file__), "templates"),
    'xsrf_cookies': True,
    'static_path':os.path.join(os.path.dirname(__file__), "static/htdocs"),
}

application = tornado.web.Application([
    (r"/", HomeHandler),
    (r"/api/v.1/([^/]+)", MainHandler),
], **settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
