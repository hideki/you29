from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    # search
    (r'^$', image_search_page),
)
