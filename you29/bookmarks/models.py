import datetime
from django.db import models
from django.contrib.auth.models import User
from you29.tags.models import Tag

###########################################################
# Models for Bookmarks
###########################################################

###########################################################
# Link Model
###########################################################
class Link(models.Model):
    """ A Link. """
    url = models.URLField(unique=True)
    def __unicode__(self):
        return self.url

###########################################################
# Bookmark Model
###########################################################
class Bookmark(models.Model):
    """ A Bookmark. """
    title = models.CharField(max_length=256)
    notes = models.TextField(blank=True)
    date  = models.DateTimeField(default=datetime.datetime.now)
    share = models.BooleanField(default=True)
    user  = models.ForeignKey(User)
    link  = models.ForeignKey(Link)
    tags  = models.ManyToManyField(Tag)
    
    class Meta:
        unique_together = (('user', 'link'),)

    def __unicode__(self):
        return '%s, %s' % (self.user.username, self.link.url)

    def get_absolute_url(self):
        return self.link.url

###########################################################
# SharedBookmark Model
###########################################################
class SharedBookmark(models.Model):
    """ A SharedBookmark. """
    link  = models.OneToOneField(Link)
    title = models.CharField(max_length=256)
    date  = models.DateTimeField(default=datetime.datetime.now)
    users = models.ManyToManyField(User)
    def __unicode__(self):
        return self.link.url
