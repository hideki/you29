[Public Tag Clouds]
select tag.name, count(tag.name) as tag_count from tags_tag tag, bookmarks_bookmark_tags bt where tag.id = bt.tag_id group by tag.name order by tag_count desc;

[everyone tags for link]
select t.name, count(t.name) as tag_count from tags_tag t, bookmarks_bookmark_tags b_t,bookmarks_bookmark b, bookmarks_link l where t.id = b_t.tag_id and b.link_id = l.id and b_t.bookmark_id = b.id and l.id = 1 group by t.name order by tag_count desc;

[User Tag Clouds]
select tag.name, count(tag.name) as tag_count from tags_tag tag, bookmarks_bookmark_tags bt,bookmarks_bookmark bookmark, auth_user user where tag.id = bt.tag_id and user.id = bookmark.user_id and bookmark.id = bt.bookmark_id and user.username='hideki' group by tag.name order by tag_count desc;
