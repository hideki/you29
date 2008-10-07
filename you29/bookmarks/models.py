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
   def shared_links(self, limit, tags=None, sortedby=None):
      join_tags = "";
      where_tags = "";
      tag_count = 0;
      for tag in tags:
         if len(tag) > 0:
            where_tags = where_tags + " AND T%d.name LIKE '%s' " % (tag_count, tag);
            join_tags = join_tags + " INNER JOIN bookmarks_bookmark_tags BT%d ON (B.id = BT%d.bookmark_id) " % (tag_count, tag_count);
            join_tags = join_tags + " INNER JOIN tags_tag T%d ON (BT%d.tag_id = T%d.id) " % (tag_count, tag_count, tag_count);
            tag_count += 1;
      order_by = "ORDER BY B.date DESC, user_count DESC";
      if sortedby == "-user_count":
         order_by = "ORDER BY user_count DESC, B.date DESC";
      query = """
         SELECT L.id, L.url, L.title, SUM(B.share) AS user_count
         FROM bookmarks_link L, bookmarks_bookmark B
         %s
         WHERE L.id = B.link_id
         %s
         GROUP BY L.id
         HAVING user_count > 0
         %s
         LIMIT %d
         """ % (join_tags, where_tags, order_by, limit);
      cursor = connection.cursor()
      cursor.execute(query);
      shared_links = [];
      for row in cursor.fetchall():
         link = self.model(id=row[0], url=row[1], title=row[2])
         link.user_count = row[3];
         shared_links.append(link);
      return shared_links;
    
   def tag_clouds(self, limit=30):
      query = """
         SELECT t.id, t.name, count(t.name) AS tag_count
         FROM tags_tag t, bookmarks_bookmark_tags b_t, bookmarks_bookmark b
         WHERE t.id = b_t.tag_id AND b.id = b_t.bookmark_id AND
         b.share = true
         GROUP BY t.name
         ORDER BY tag_count DESC
         LIMIT %d
         """ % (limit);
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
      if(self.user_count() > 5):
         return True;
      else:
         return False;

   def user_count(self):
      return self.bookmark_set.filter(share=True).count();

   def get_tags(self):
      query = """
         SELECT t.id, t.name, count(t.name) as tag_count
         FROM tags_tag t, bookmarks_bookmark_tags b_t,
         bookmarks_bookmark b, bookmarks_link l
         WHERE t.id = b_t.tag_id AND b.link_id = l.id AND
         b_t.bookmark_id = b.id AND b.share = true AND l.id = %d
         GROUP BY t.name
         ORDER BY tag_count DESC
         """ % (self.id);
      cursor = connection.cursor()
      cursor.execute(query);
      tags = [];
      for row in cursor.fetchall():
         tag = CustomTag(row[0], row[1], row[2])
         tags.append(tag);
      return tags;

###########################################################
# Manager for Bookmark Model
###########################################################
class BookmarkManager(models.Manager):
   def tag_clouds(self, username, is_owner):
      logging.debug("tag_clouds username=%s is_owner=%s" % (username, is_owner));
      if not is_owner:
         query = """
            SELECT t.id, t.name, count(t.name) AS tag_count
            FROM tags_tag t, bookmarks_bookmark_tags b_t,
            bookmarks_bookmark b, auth_user u
            WHERE t.id = b_t.tag_id 
            and u.id = b.user_id
            and b.id = b_t.bookmark_id 
            and b.share = true
            and u.username=%s
            GROUP BY t.name
            ORDER BY tag_count DESC""";
      else:
         query = """
            SELECT t.id, t.name, count(t.name) AS tag_count
            FROM tags_tag t, bookmarks_bookmark_tags b_t,
            bookmarks_bookmark b, auth_user u
            WHERE t.id = b_t.tag_id 
            and u.id = b.user_id
            and b.id = b_t.bookmark_id 
            and u.username=%s
            GROUP BY t.name
            ORDER BY tag_count DESC""";
      cursor = connection.cursor()
      cursor.execute(query, [username]);
      tag_clouds = [];
      for row in cursor.fetchall():
         tag = CustomTag(row[0], row[1], row[2])
         tag_clouds.append(tag);
      return tag_clouds;

   def associated_tags(self, **kwargs): 
      ids = kwargs['ids'];
      if len(ids) == 0:
         return [];
      tags = kwargs['tags'];
      in_ids = "";
      for id in ids:
         if len(in_ids) == 0:
            in_ids = str(id);
         else:
            in_ids = in_ids + ", " +str(id);
      where_tags = "";
      for tag in tags:
         if len(tag) > 0:
            where_tags = where_tags + " AND T.name NOT LIKE '%s' " % ( tag);
      query = """
         SELECT T.id, T.name, count(T.name) AS tag_count
         FROM tags_tag T, bookmarks_bookmark_tags BT, bookmarks_bookmark B
         WHERE T.id = BT.tag_id AND B.id = BT.bookmark_id 
         AND B.id in (%s)
         %s
         GROUP BY T.name
         ORDER BY tag_count DESC
         """ %(in_ids, where_tags);
      cursor = connection.cursor()
      cursor.execute(query);
      associated_tags = [];
      for row in cursor.fetchall():
         tag = CustomTag(row[0], row[1], row[2])
         associated_tags.append(tag);
      return associated_tags;

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
