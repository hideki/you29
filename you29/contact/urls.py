from django.conf.urls.defaults import *
from views import contact

urlpatterns = patterns('',
    (r'^$',  contact),
)
