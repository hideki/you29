import logging
#from urllib import urlopen, urlencode
import urllib
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from forms import *
from models import Bookmark, Link, Tag
from django.conf import settings

def i18n_config(request):
    variables = RequestContext(request, {
        'LANGUAGES':settings.LANGUAGES,
    });
    return render_to_response('bookmarks/i18n_page.html', variables)

def main_page(request):
    logging.debug("bookmarks.views.main_page()");
    logging.debug("lang_code: %s" % request.LANGUAGE_CODE);
    if request.user.is_authenticated():
        return user_page(request, request.user.username)
    else:
        return public_page(request)

def public_page(request):
    logging.debug("bookmarks.views.public_page()");
    http_host = request.META['HTTP_HOST']
    links = Link.objects.order_by('-id')[:30];
    tags  = Link.objects.tag_clouds()[:30];
    variables = RequestContext(request, {
        'page_type':'public',
        'links':links,
        'tags':tags,
        'http_host':http_host
    })
    return render_to_response('bookmarks/bookmarks_page.html', variables)

def user_page(request, username):
    logging.debug("bookmarks.views.user_page() username=%s" % (username));
    logging.debug("bookmarks.views.user_page() request.user.username=%s" %
      (request.user.username));
    user = get_object_or_404(User, username=username)
    http_host = request.META['HTTP_HOST']
    tags = Bookmark.objects.tag_clouds(username);
    if(user.username == request.user.username):
        is_owner = True;    
        bookmarks = user.bookmark_set.order_by('-date')
        show_edit = True
        show_delete = True
    else:
        is_owner = False;    
        bookmarks = user.bookmark_set.filter(share=True).order_by('-date')
        show_edit   = False
        show_delete = False
    variables = RequestContext(request, {
        'page_type':'user',
        'is_owner': is_owner,
        'user': request.user,
        'username':username,
        'bookmarks':bookmarks,
        'tags':tags,
        'show_edit':show_edit,
        'show_delete':show_delete,
        'http_host':http_host
    })
    return render_to_response('bookmarks/bookmarks_page.html', variables)

# Add Bookmark
def add_bookmark(request):
    logging.debug("bookmarks.views.add_bookmark()");
    if not request.user.is_authenticated():
        url = request.path + '?' + request.META['QUERY_STRING'];
        url = urllib.quote(url);
        return HttpResponseRedirect('/accounts/login/?next=%s' % url)
    if(request.GET.has_key('url') and request.GET.has_key('title')):
        url   = request.GET['url']
        title = request.GET['title']
        form  = BookmarkSaveForm({'url':url,'title':title, 'share':True})
    else:
        form = BookmarkSaveForm(initial={'share':True})

    popup = False;
    if(request.GET.has_key('_popup')):
        popup = bool(request.GET['_popup']);
    variables = RequestContext(request, {'form':form, 'popup':popup})
    return render_to_response('bookmarks/save_page.html', variables)

# Edit Bookmark
def edit_bookmark(request, bookmark_id):
    logging.debug("bookmarks.views.edit_bookmark() bookmark_id=%s" % (bookmark_id));
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)
    bookmark = get_object_or_404(Bookmark, id=bookmark_id)
    url      = bookmark.link.url
    title    = bookmark.title
    tags     = ' '.join(tag.name for tag in bookmark.tags.all())
    notes    = bookmark.notes
    share    = bookmark.share;
    form     = BookmarkSaveForm({'url':url,'title':title,'tags':tags, 'notes':notes, 'share':share})
    variables = RequestContext(request, {'form':form})
    return render_to_response('bookmarks/save_page.html', variables)

# Delete Bookmark
def delete_bookmark(request, bookmark_id):
    logging.debug("bookmarks.views.delete_bookmark() bookmark_id=%s" % (bookmark_id));
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)
    bookmark = get_object_or_404(Bookmark, id=bookmark_id)
    if(bookmark.user.username == request.user.username):
        link = bookmark.link;
        bookmark.delete();
        if(link.bookmark_set.count() == 0):
            link.delete();
    return HttpResponseRedirect('/bookmarks/user/%s' % request.user.username)

# Save Bookmark
def save_bookmark(request):
    logging.debug("bookmarks.views.save_bookmark()");
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)
    if request.method == 'POST':
        form = BookmarkSaveForm(request.POST)
        if form.is_valid():
            bookmark = _save_bookmark(request, form)
            popup = False;
            if(request.POST.has_key('_popup')):
                logging.debug("popup=%s" % request.POST['_popup']);
                popup = bool(request.POST['_popup']);
                logging.debug("popup=%d" % popup);
            logging.debug("bookmarks.views.save_bookmark() popup=%s" % popup);
            if(popup):
                return render_to_response('bookmarks/close_page.html')
            else:
                return HttpResponseRedirect('/bookmarks/user/%s' % request.user.username)
    variables = RequestContext(request, {'form':form})
    return render_to_response('bookmarks/save_page.html', variables)

def _save_bookmark(request, form):
    logging.debug("bookmarks.views._save_bookmark()");
    # Create or get link.
    link, created = Link.objects.get_or_create(url=form.cleaned_data['url'])
    if created:
        link.title = form.cleaned_data['title']
        link.save()
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
    # Save bookmark to database
    bookmark.save()
    return bookmark;
