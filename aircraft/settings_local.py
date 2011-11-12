#-*- coding: utf-8 -*-

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'aircraft',                   # Or path to database file if using sqlite3.
        'USER': 'root',                       # Not used with sqlite3.
        'PASSWORD': '',                       # Not used with sqlite3.
        'HOST': '',                           # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                           # Set to empty string for default. Not used with sqlite3.
    }
}

DEBUG = False
TEMPLATE_DEBUG = DEBUG

import sys
if 'test' in sys.argv:
    DATABASES['default']['ENGINE'] = 'sqlite3'
    INSTALLED_APPS = tuple(INSTALLED_APPS[1:])

#INTERNAL_IPS = ('127.0.0.1',)
#MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
#INSTALLED_APPS += ('debug_toolbar',)

NOSE_ARGS = [
#              '--stop',
              '--nocapture',
#              '-a tags=dev',
              '--with-id',
#              '--failed',
#              '--processes=4',
    
]

#NOSE_PLUGINS = [ 'nose.plugins.multiprocess.MultiProcess' ]

SECRET_KEY = 'ryasdgftbvha4trkj7b59i&342f105h+yrus(sfjsupie(mwz3'


