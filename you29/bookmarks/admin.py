from django.contrib import admin
from models import Tag, Link, Bookmark

class TagAdmin(admin.ModelAdmin):
    pass

class LinkAdmin(admin.ModelAdmin):
    pass

class BookmarkAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tag,      TagAdmin)
admin.site.register(Link,     LinkAdmin)
admin.site.register(Bookmark, BookmarkAdmin)
