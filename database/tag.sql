[Public Tag Clouds]
select tag.name, count(tag.name) as tag_count from tags_tag tag, bookmarks_bookmark_tags bt where tag.id = bt.tag_id group by tag.name order by tag_count desc;

[User Tag Clouds]
select tag.name, count(tag.name) as tag_count from tags_tag tag, bookmarks_bookmark_tags bt,bookmarks_bookmark bookmark, auth_user user where tag.id = bt.tag_id and user.id = bookmark.user_id and bookmark.id = bt.bookmark_id and user.username='hideki' group by tag.name order by tag_count desc;
