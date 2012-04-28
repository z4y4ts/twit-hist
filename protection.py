#!/usr/bin/env python3

"""
Twitter History @ DOU Hack

This script protects secure areas
"""

import cherrypy

def setCookie(name, value, path = '/', expires = None, max_age = 3600, version = 1):
    cherrypy.response.cookie[name] = value
    if path is not None:
        cherrypy.response.cookie[name]['path'] = path
    if expires is not None:
        cherrypy.response.cookie[name]['expires'] = expires
    if max_age is not None:
        cherrypy.response.cookie[name]['max-age'] = max_age
    if version is not None:
        cherrypy.response.cookie[name]['version'] = version

def readCookie(name):
    return cherrypy.request.cookie[name].value if name in cherrypy.request.cookie else None

def rmCookie(name):
    setCookie(name = name, value = 'expired', path = None, expires = 0, max_age = None, version = None)

def checkCookie(name):
    return name in cherrypy.request.cookie

def str2date(timestring, time_format = '%Y-%m-%d %H:%M:%S'):
    import time, datetime
    #print(timestring)
    #print('test:', datetime.datetime.fromtimestamp(time.mktime(time.strptime(timestring, time_format))))
    return datetime.datetime.fromtimestamp(time.mktime(time.strptime(timestring, time_format)))

class DB:
    # configure our database connection here
    __connection__ = '' #connection string here
    
    connection = None
           
    def connect(self):
        #from sqlalchemy import create_engine
        #self.connection = create_engine(self.__connection__)
        #print(self.connection)
        pass
    
    def query(self, sql):
        #pass
        #from sqlalchemy.exc import DBAPIError, SQLAlchemyError
        fails_counter = 0
        while True:
            try:
                #print('============== QUERYING ==============')
                #self.connection.ping(True)
                #print(sql)
                #return self.connection.execute(sql)
                #print('|============! QUERYING !============|')
                #break
                pass
            except: # DBAPIError as e:
               #print('DB Exception', e)
                fails_counter += 1
                if fails_counter < 3:
                    pass
                    #self.connection.execute('select 1;')
                else:
                    raise cherrypy.HTTPError(500, 'Неможливо з’єднатися з БД :(')
        try:
            return self.connection.fetchall()
        except: #SQLAlchemyError:
           #print('sq')
            return self

db = DB()
db.connect()

def protect():
    #if (not cherrypy.request.path_info.startswith('/admin')):
    #    #print('No protection')
    #    return
    #print(cherrypy.request.cookie)
    try: # check VK GET/cookie here
    #if cherrypy.request.login not in users:
        #raise cherrypy.HTTPError("401 Unauthorized")
        from hashlib import md5
        #cherrypy.session['user'] = None #debug
        redirect = readCookie('redirect')
        
        #print(redirect)
        
        if redirect is not None:
            rmCookie('redirect')
            #print('Redirecting to ', redirect)
            raise cherrypy.HTTPRedirect(redirect)

        #if cherrypy.session['user'].get('logged',None) != 'in':
        #    raise cherrypy.HTTPError("401 Unauthorized")

    except cherrypy.HTTPRedirect as e:
        #print('Redirecting handled')
        raise e
    except Exception as e:
        #print('Authorization failed:', e)
        #print(cherrypy.session.get('user'))
        if not cherrypy.request.path_info.startswith('/admin'):
            #print('No protection')
            return
        #setCookie('redirect', cherrypy.request.path_info, expires = 333000000)
        #raise cherrypy.HTTPRedirect('/login')#, IK92.error(None,code = 401))
        #raise cherrypy.HTTPError('401 Unauthorized', 'Authorize here http://vk.com/app{0}'.format(VK_API_ID))#, IK92.error(None,code = 401))
        pass #<irony>give it up :D</irony>
