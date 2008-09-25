--
-- Delete all records in django_admin_log
delete from django_admin_log;

--
-- Add title column into bookmarks_link table
--
alter table bookmarks_link add title varchar(256) not null;

--
-- Update title column of link from bookmark tilte]
--
update bookmarks_link l, bookmarks_bookmark b set l.title = b.title where l.id = b.link_id;

--
-- drop sharedbookmark table]
--
drop table bookmarks_sharedbookmark_users;
drop table bookmarks_sharedbookmark;
