from django.contrib import admin
from you29.tags.models import Tag

class TagAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tag, TagAdmin)
