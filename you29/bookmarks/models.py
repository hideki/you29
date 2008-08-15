from django.db import models
from django.contrib.auth.models import User


###########################################################
# Models for Bookmarks
###########################################################

###########################################################
# Tag Model
###########################################################
class Tag(models.Model):
    """ A tag. """
    name = models.CharField(max_length=64, unique=True)
    def __unicode__(self):
        return self.name
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
    notes = models.TextField()
    date  = models.DateTimeField(auto_now_add=True)
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
