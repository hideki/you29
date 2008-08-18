import logging
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from forms import BookmarkSaveForm
from models import Bookmark, Link, SharedBookmark, Tag

def main_page(request):
    logging.debug("bookmarks.views.main_page()");
    bookmarks = SharedBookmark.objects.order_by('-date')[:30]
    variables = RequestContext(request, { 'bookmarks':bookmarks })
    return render_to_response('bookmarks/main_page.html', variables)

def user_page(request, username):
    logging.debug("bookmarks.views.user_page() username=%s" % (username));
    user = get_object_or_404(User, username=username)
    bookmarks = user.bookmark_set.order_by('-date')
    show_edit   = False
    show_delete = False
    if(user.username == request.user.username):
        show_edit = True
        show_delete = True
    variables = RequestContext(request, {
        'user': request.user,
        'username':username,
        'bookmarks':bookmarks,
        'show_edit':show_edit,
        'show_delete':show_delete
    })
    return render_to_response('bookmarks/user_page.html', variables)

@login_required
def delete_page(request, bookmark_id):
    logging.debug("bookmarks.views.delete_page() bookmark_id=%s" % (bookmark_id));
    bookmark = get_object_or_404(Bookmark, id=bookmark_id)
    logging.debug("bookmarks.views.delete_page() bookmark=%s" % (bookmark));
    if(bookmark.user.username == request.user.username):
        bookmark.delete()
    return HttpResponseRedirect('/bookmarks/user/%s' % request.user.username)


@login_required
def save_page(request):
    logging.debug("bookmarks.views.save_page()");
    # Save Bookmark
    if request.method == 'POST':
        form = BookmarkSaveForm(request.POST)
        if form.is_valid():
            bookmark = _bookmark_save(request, form)
            return HttpResponseRedirect('/bookmarks/user/%s' % request.user.username)
    # Update Bookmark Form
    elif request.GET.has_key('url'):
        url = request.GET['url']
        title = ''
        tags  = ''
        notes = ''
        share = True;
        try:
            link = Link.objects.get(url=url)
            bookmark = Bookmark.objects.get(link=link, user=request.user)
            title = bookmark.title
            tags  = ' '.join(tag.name for tag in bookmark.tags.all())
            notes = bookmark.notes
            share = bookmark.share;
        except ObjectDoesNotExist:
            pass
        form = BookmarkSaveForm({'url':url,'title':title,'tags':tags, 'notes':notes, 'share':share})
    # New Bookmark Form
    else:
        form = BookmarkSaveForm()
    variables = RequestContext(request, {'form':form})
    return render_to_response('bookmarks/save_page.html', variables)


def _bookmark_save(request, form):
    logging.debug("bookmarks.views._bookmark_save()");
    # Create or get link.
    link, dummy = Link.objects.get_or_create(url=form.cleaned_data['url'])
    # Create or get bookmark with user and link
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, link=link)
    # Update bookmark title
    bookmark.title = form.cleaned_data['title']
    # Update bookmark notes
    bookmark.notes = form.cleaned_data['notes']
    # Update bookmark share
    bookmark.share = form.cleaned_data['share']
    # If the bookmark is being updated, clear old tag list.
    if not created:
        bookmark.tags.clear()
    # Create new tag list
    tag_names = form.cleaned_data['tags'].split()
    for tag_name in tag_names:
        tag, dummy = Tag.objects.get_or_create(name=tag_name)
        bookmark.tags.add(tag)
    # Share Bookmark
    if bookmark.share:
        shared_bookmark, created = SharedBookmark.objects.get_or_create(link=bookmark.link)
        if created:
            shared_bookmark.title = bookmark.title
        shared_bookmark.users.add(request.user)
        shared_bookmark.save()
    # Not Share Bookmark
    else:
        try:
            shared_bookmark = SharedBookmark.objects.get(link=bookmark.link)
            shared_bookmark.users.remove(request.user)
            logging.debug("%s" % (shared_bookmark.users.count()))
            if(shared_bookmark.users.count() == 0):
                shared_bookmark.delete()
            else:
                shared_bookmark.save()
        except ObjectDoesNotExist:
            pass;
    # Save bookmark to database
    bookmark.save()
    return bookmark;
