from django.contrib import admin
from models import Link, Bookmark, SharedBookmark 

class LinkAdmin(admin.ModelAdmin):
    pass

class BookmarkAdmin(admin.ModelAdmin):
    pass

class SharedBookmarkAdmin(admin.ModelAdmin):
    pass

admin.site.register(Link, LinkAdmin)
admin.site.register(Bookmark, BookmarkAdmin)
admin.site.register(SharedBookmark, SharedBookmarkAdmin)
