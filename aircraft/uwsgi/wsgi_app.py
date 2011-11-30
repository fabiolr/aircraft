#!/home/aircraft/aircraft/aircraft-env/bin/python
import sys, os
#sys.path.append('/home/aircraft/aircraft')
sys.path.append('/home/aircraft/aircraft/aircraft')

import django.core.handlers.wsgi
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
application = django.core.handlers.wsgi.WSGIHandler()
