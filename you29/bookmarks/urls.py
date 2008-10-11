from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
   # Bookmark browsing
   (r'^$', main_page),
   (r'^public/$', public_page),
   (r'^public/(.+)$', public_tag_page),
   (r'^user/(\w+)/$', user_page),
   (r'^user/(\w+)/(.+)/$', user_tag_page),
   (r'^link/(\d+)/$', link_page),

   # Search
   (r'^public_search/$', public_search_bookmarks),
   (r'^search/(\w+)/$', search_bookmarks),

   # Bookmark management
   (r'^add/$',          add_bookmark),
   (r'^copy/(\d+)/$',   copy_bookmark),
   (r'^edit/(\d+)/$',   edit_bookmark),
   (r'^delete/(\d+)/$', delete_bookmark),
   (r'^save/$',         save_bookmark),

   # internationalization
   (r'^i18n/$',         i18n_config),
)
