from django.contrib import admin
from models import Link, Bookmark

class LinkAdmin(admin.ModelAdmin):
    pass

class BookmarkAdmin(admin.ModelAdmin):
    pass

admin.site.register(Link, LinkAdmin)
admin.site.register(Bookmark, BookmarkAdmin)
