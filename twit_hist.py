#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Twitter History @ DOU Hack

Twitter history caching project
"""

import sys
import os.path
CURRENT_DIR = os.path.dirname(__file__)
sys.path.append(CURRENT_DIR)

import cherrypy

import protection

db = protection.db

cherrypy.tools.protect = cherrypy.Tool('before_handler', protection.protect)

from jinja2 import Environment, PackageLoader
twi_env = Environment(loader=PackageLoader('twit_hist', 'static/tpl/'))

import locale
locale.setlocale(locale.LC_ALL, 'uk_UA')

GLOBAL_STRINGS = {'version_stage': 'pre-alpha', 'sitetitle': 'Twitter History'}

class TwiHist:
    _cp_config = {'tools.sessions.on': True}
    
    @cherrypy.expose
    def index(self, name = None):
        # Increase the silly hit counter
        count = cherrypy.session.get('count', 0) + 1
        # Store the new value in the session dictionary
        cherrypy.session['count'] = count

        # Ask for the user's name.
        if name is not None:
            cherrypy.session['name'] = name
        
        articles = db.getArticles()
        return twi_env.get_template('articles/list/index.tpl').render(GLOBAL_STRINGS, articles = articles)

    @cherrypy.expose
    def login(self, **kwargs):
        return twi_env.get_template('login.tpl').render(GLOBAL_STRINGS, pagetitle = 'Вхід', user = cherrypy.session.get('user', None))
    
    @cherrypy.expose
    def logout(self, hash = None, **kwargs):
        if cherrypy.session.get('user', None) is None or len(kwargs) > 0 or hash is None or hash != cherrypy.session['user'].get('logout_hash', None):
            yield 'Ха-ха! Тебе спробували розвести на logout :D'
        else:
            yield twi_env.get_template('logout.tpl').render(local_title='Бувай!', title='Ще побачимось')
            cherrypy.lib.sessions.expire()

    @cherrypy.expose
    def default(self, x=None):
        return 'Error: Cannot parse following URL ' + x + '. Trying to get required article'

class Admin:
    @cherrypy.expose
    def index(self):
        raise cherrypy.HTTPRedirect('news')
        return twi_env.get_template('admin/news/index.tpl').render(GLOBAL_STRINGS, pagetitle = 'Адмінка', user = cherrypy.session.get('user', None))

    @cherrypy.expose
    def default(self, **kwargs):
        raise cherrypy.HTTPRedirect('news')

TwiHist.admin = Admin()

conf = os.path.join(CURRENT_DIR, 'twit_hist.conf')

if __name__ == '__main__':
    cherrypy.quickstart(TwiHist(), config=conf)
else:
    cherrypy.tree.mount(TwiHist(), config=conf)

