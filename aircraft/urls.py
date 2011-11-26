from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.views.generic.simple import redirect_to

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'aircraft.views.home', name='home'),
                       # url(r'^aircraft/', include('aircraft.foo.urls')),
                       
                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       
                       
                       # Uncomment the next line to enable the admin:
                       url(r'^admin/finance/aircraft.xls', 'finance.views.report'),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^admin_tools/', include('admin_tools.urls')),
                       url(r'^$', redirect_to, {'url': '/admin/'}),
                       )

urlpatterns += staticfiles_urlpatterns()
