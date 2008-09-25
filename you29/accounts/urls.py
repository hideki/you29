from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from views import register_page

urlpatterns = patterns('',
    (r'^register/$',                register_page),
    (r'^logout/$',                  'django.contrib.auth.views.logout', {'next_page':'/'}),
    (r'^login/$',                   'django.contrib.auth.views.login',                {'template_name': 'accounts/login.html'}),
    (r'^password_reset/$',          'django.contrib.auth.views.password_reset'),
    (r'^password_reset_done/$',     'django.contrib.auth.views.password_reset_done'),
    (r'^password_reset_confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',  'django.contrib.auth.views.password_reset_confirm'),
    (r'^password_reset_complete/$', 'django.contrib.auth.views.password_reset_complete'),
    (r'^password_change/$',         'django.contrib.auth.views.password_change'),
    (r'^password_change_done/$',    'django.contrib.auth.views.password_change_done'),
)
