from django.conf.urls.defaults import *
from django.contrib import admin
from home.views import main_page

# For Admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^you29/', include('you29.foo.urls')),

    # Uncomment the next line to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line for to enable the admin:
    (r'^admin/(.*)', admin.site.root),
    (r'^$', main_page),
)
