from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from views import *

urlpatterns = patterns('',
    (r'^login/$', 'django.contrib.auth.views.login',
        {'template_name':'accounts/login.html'}),
    (r'^logout/$', logout_page),
    (r'^register/$', register_page),
)
