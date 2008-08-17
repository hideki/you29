import logging
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from forms import BookmarkSaveForm
from models import Bookmark, Link, Tag

def main_page(request):
    logging.debug("bookmarks.views.main_page()");
    variables = RequestContext(request, {
        'user': request.user
    })
    return render_to_response('bookmarks/main_page.html', variables)

def user_page(request, username):
    logging.debug("bookmarks.views.user_page() username=%s" % (username));
    user = get_object_or_404(User, username=username)
    bookmarks = user.bookmark_set.order_by('-date')
    variables = RequestContext(request, {
        'username':username,
        'bookmarks':bookmarks
    })
    return render_to_response('bookmarks/user_page.html', variables)


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
        tags = ''
        notes = ''
        try:
            link = Link.objects.get(url=url)
            bookmark = Bookmark.objects.get(link=link, user=request.user)
            title = bookmark.title
            tags  = ' '.join(tag.name for tag in bookmark.tag_set.all())
            notes = bookmark.notes
        except ObjectDoesNotExist:
            pass
        form = BookmarkSaveForm({'url':url,'title':title,'tags':tags, 'notes':notes})
    # New Bookmark Form
    else:
        form = BookmarkSaveForm()
    variables = RequestContext(request, {'form':form})
    return render_to_response('bookmarks/save_page.html', variables)

def _bookmark_save(request, form):
    logging.debug("bookmarks.views._bookmark_save");
    # Create or get link.
    link, dummy = Link.objects.get_or_create(url=form.cleaned_data['url'])
    # Create or get bookmark
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, link=link)
    # Update bookmark title
    bookmark.title = form.cleaned_data['title']
    # Update bookmark notes
    bookmark.notes = form.cleaned_data['notes']
    # If the bookmark is being updated, clear old tag list.
#    if not created:
#        bookmark.tag_set.clear()
#    # Create new tag list
#    tag_names = form.cleaned_data['tags'].split()
#    for tag_name in tag_names:
#        tag, dummy = Tag.objects.get_or_create(name=tag_name)
#        bookmark.tag_set.add(tag)
#    # Share on the main page if requested.
#    if form.cleaned_data['share']:
#        shared_bookmark, created = SharedBookmark.objects.get_or_create(
#            bookmark=bookmark)
#        if created:
#            shared_bookmark.users_voted.add(request.user)
#            shared_bookmark.save()
    # Save bookmark to database
    bookmark.save()
    return bookmark;
