from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    # Bookmark browsing
    (r'^$', main_page),
    (r'^user/(\w+)/$', user_page),

    # Bookmark management
    (r'^save/$',         save_page),
    (r'^delete/(\d+)/$', delete_page),
)
