import logging
import datetime
from django.db import models, connection
from django.contrib.auth.models import User
from you29.tags.models import Tag

###########################################################
# Models for Bookmarks
###########################################################

class CustomTag():
    def __init__(self, id, name, count):
        self.id = id;
        self.name = name;
        self.count = count;

###########################################################
# Manager for Link Model
###########################################################
class LinkManager(models.Manager):
    def tag_clouds(self):
        query = """
            SELECT t.id, t.name, count(t.name) AS tag_count
            FROM tags_tag t, bookmarks_bookmark_tags bt
            WHERE t.id = bt.tag_id 
            GROUP BY t.name
            ORDER BY tag_count desc""";
        cursor = connection.cursor()
        cursor.execute(query);
        tag_clouds = [];
        for row in cursor.fetchall():
            tag = CustomTag(row[0], row[1], row[2])
            tag_clouds.append(tag);
        return tag_clouds;


###########################################################
# Link Model
###########################################################
class Link(models.Model):
    """ A Link. """
    url   = models.URLField(unique=True)
    title = models.CharField(max_length=256)
    
    objects = LinkManager();

    def __unicode__(self):
        return self.url
    def is_popular(self):
        logging.debug("Link.is_popular()")
        if(self.bookmark_set.count() > 5):
            return True;
        else:
            return False;

###########################################################
# Manager for Bookmark Model
###########################################################
class BookmarkManager(models.Manager):
    def tag_clouds(self, username):
        query = """
            SELECT tag.id, tag.name, count(tag.name) AS tag_count
            FROM tags_tag tag, bookmarks_bookmark_tags bt,
            bookmarks_bookmark bookmark, auth_user user
            WHERE tag.id = bt.tag_id 
            and user.id = bookmark.user_id
            and bookmark.id = bt.bookmark_id 
            and user.username=%s
            GROUP BY tag.name
            ORDER BY tag_count desc""";
        cursor = connection.cursor()
        cursor.execute(query, [username]);
        tag_clouds = [];
        for row in cursor.fetchall():
            tag = CustomTag(row[0], row[1], row[2])
            tag_clouds.append(tag);
        return tag_clouds;
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

    objects = BookmarkManager();
    
    class Meta:
        unique_together = (('user', 'link'),)

    def __unicode__(self):
        return '%s, %s' % (self.user.username, self.link.url)

    def get_absolute_url(self):
        return self.link.url

    def is_popular(self):
        return self.link.is_popular();
