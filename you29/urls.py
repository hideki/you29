import os.path
from django.conf.urls.defaults import *
from django.contrib import admin

#For Media files
site_media = os.path.join(
    os.path.dirname(__file__), 'site_media'
)

# For Admin
admin.autodiscover()

urlpatterns = patterns('',
    # site_media
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': site_media}),

    # admin page
    (r'^admin/(.*)', admin.site.root),

    # main
    (r'^', include('you29.main.urls')),

    # users
    (r'^users/', include('you29.users.urls')),

    # bookmarks
    (r'^bookmarks/', include('you29.bookmarks.urls')),
)