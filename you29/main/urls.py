from django.conf.urls.defaults import *
from views import main_page

urlpatterns = patterns('',
    (r'^$', main_page),
)
