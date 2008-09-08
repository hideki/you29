from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    # Bookmark browsing
    (r'^$', main_page),
    (r'^public/$', public_page),
    (r'^public/(\w+)/$', public_tag_page),
    (r'^user/(\w+)/$', user_page),
    (r'^user/(\w+)/(\w+)/$', user_tag_page),

    # Bookmark management
    #(r'^new/$',          new_bookmark),
    (r'^add/$',          add_bookmark),
    (r'^edit/(\d+)/$',   edit_bookmark),
    (r'^delete/(\d+)/$', delete_bookmark),
    (r'^save/$',         save_bookmark),

    # internationalization
    (r'^i18n/$',         i18n_config),
)
