import logging
import urllib
import re
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from forms import BookmarkSaveForm
from models import Bookmark, Link, Tag

ITEMS_PER_PAGE = 25;

def i18n_config(request):
  variables = RequestContext(request, {
		'script_name':request.META['SCRIPT_NAME'],
		'LANGUAGES':settings.LANGUAGES, });
  return render_to_response('bookmarks/i18n_page.html', variables)

def main_page(request):
  logging.debug("bookmarks.views.main_page()");
  logging.debug("lang_code: %s" % request.LANGUAGE_CODE);
  if request.user.is_authenticated():
    return HttpResponseRedirect(reverse('you29.bookmarks.views.user_page',args=(request.user.username,)))
  else:
    return HttpResponseRedirect(reverse('you29.bookmarks.views.public_page'))
   
def link_page(request, link_id):
  logging.debug("bookmarks.views.link_page() link_id=%s" % (link_id));
  http_host = request.META['HTTP_HOST']
  link      = Link.objects.get(id__exact=link_id);
  bookmarks = Bookmark.objects.filter(link=link).filter(share=True).order_by('-date');
  tags      = Link.objects.tag_clouds(30);
  variables = RequestContext(request, {
		'script_name':request.META['SCRIPT_NAME'],
    'page_type':'link',
    'content_type':'public',
    'count': len(bookmarks),
    'link':link,
    'bookmarks':bookmarks,
    'tags':tags,
    'http_host':http_host,
    'show_save':True
  });
  return render_to_response('bookmarks/bookmarks_page.html', variables)

def public_page(request):
  logging.debug("bookmarks.views.public_page()");
  http_host = request.META['HTTP_HOST']
  if request.GET.has_key('linksortedby'):
    request.session['linksortedby'] = request.GET['linksortedby'];
  linksortedby = request.session.get('linksortedby', "-date");
  links = Link.objects.shared_links(30, [], linksortedby);
  tags  = Link.objects.tag_clouds(30);
  variables = RequestContext(request, {
		'script_name':request.META['SCRIPT_NAME'],
    'page_type':'public',
    'content_type':'public',
    'linksortedby':linksortedby,
    'links':links,
    'tags':tags,
    'http_host':http_host,
    'show_save':True
  })
  return render_to_response('bookmarks/bookmarks_page.html', variables)

def public_tag_page(request, tags):
  logging.debug("bookmarks.views.public_tag_page() tags=%s" % (tags));
  http_host = request.META['HTTP_HOST'];
  tag_array = tags.split('/');
  if request.GET.has_key('linksortedby'):
    request.session['linksortedby'] = request.GET['linksortedby'];
  linksortedby = request.session.get('linksortedby', "-date");
  links = Link.objects.shared_links(30, tag_array, linksortedby);
  tags  = Link.objects.tag_clouds(30);
  tag_nav = [];
  url = "/bookmarks/public/";
  for tag in tag_array:
    if(len(tag) > 0):
      url += tag + "/";
      tag_dict = {'name': tag, 'url': url};
      tag_nav.append(tag_dict);
  variables = RequestContext(request, {
		'script_name':request.META['SCRIPT_NAME'],
    'page_type':'public',
    'content_type':'public',
    'linksortedby':linksortedby,
    'links':links,
    'tags':tags,
    'tag_nav':tag_nav,
    'http_host':http_host,
    'show_save':True
  })
  return render_to_response('bookmarks/bookmarks_page.html', variables)

def user_page(request, username):
  logging.debug("bookmarks.views.user_page() request.META['SCRIPT_NAME']=%s" % (request.META['SCRIPT_NAME']));
  logging.debug("bookmarks.views.user_page() request.path=%s" % (request.path));
  logging.debug("bookmarks.views.user_page() username=%s" % (username));
  logging.debug("bookmarks.views.user_page() request.user.username=%s" % (request.user.username));
  http_host = request.META['HTTP_HOST']
  user = get_object_or_404(User, username=username)
  if request.GET.has_key('sortedby'):
    request.session['sortedby'] = request.GET['sortedby'];
  sortedby = request.session.get('sortedby', "-date");
  if(user.username == request.user.username):
    bookmarks = Bookmark.objects.filter(user=user).order_by(sortedby);
    is_owner = True;    
    show_edit = True;
    show_delete = True;
    show_save=False;
  else:
    bookmarks = Bookmark.objects.filter(user=user).filter(share=True).order_by(sortedby);
    is_owner = False;    
    show_edit   = False
    show_delete = False
    show_save   =True;
  tags = Bookmark.objects.tag_clouds(username, is_owner)[:30];
  paginator = Paginator(bookmarks, ITEMS_PER_PAGE);
  page = 1;
  if request.GET.has_key('page'):
    page = int(request.GET['page']);
  try:
    p = paginator.page(page);
  except:
    raise Http404;
  variables = RequestContext(request, {
		'script_name':request.META['SCRIPT_NAME'],
    'page_type':'user',
    'content_type':'user',
    'sortedby':sortedby,
    'is_owner': is_owner,
    'user': request.user,
    'username':username,
    'bookmarks':p.object_list,
    'total':len(bookmarks),
    'tags':tags,
    'show_edit':show_edit,
    'show_delete':show_delete,
    'show_save':show_save,
    'http_host':http_host,
    'has_other_pages': p.has_other_pages(),
    'has_next': p.has_next(),
    'has_previous': p.has_previous(),
    'page': p.number,
    'pages': range(1, p.paginator.num_pages + 1),
    'next_page_number': p.next_page_number(),
    'previous_page_number': p.previous_page_number()
  })
  return render_to_response('bookmarks/bookmarks_page.html', variables)

def user_tag_page(request, username, tags):
  logging.debug("bookmarks.views.user_tag_page() username=%s tags=%s" % (username, tags));
  logging.debug("bookmarks.views.user_tag_page() request.user.username=%s" % (request.user.username));
  tag_array = tags.split('/');
  if request.GET.has_key('sortedby'):
    request.session['sortedby'] = request.GET['sortedby'];
  sortedby = request.session.get('sortedby', "-date");
  user = get_object_or_404(User, username=username)
  http_host = request.META['HTTP_HOST']
  if(user.username == request.user.username):
    bookmarks = Bookmark.objects.filter(user=user);
    for tag in tag_array:
      if len(tag) > 0:
        bookmarks = bookmarks.filter(Q(**{'tags__name__iexact':tag}));
    bookmarks = bookmarks.order_by(sortedby);
    is_owner    = True;    
    show_edit   = True;
    show_delete = True;
    show_save   = False;
  else:
    bookmarks = Bookmark.objects.filter(user=user).filter(share=True);
    for tag in tag_array:
      if len(tag) > 0:
        bookmarks = bookmarks.filter(Q(**{'tags__name__iexact':tag}));
    bookmarks = bookmarks.order_by(sortedby);
    is_owner    = False;    
    show_edit   = False;
    show_delete = False;
    show_save   = True;
  ids = [];
  for bookmark in bookmarks:
    ids.append(bookmark.id);
  tags = Bookmark.objects.associated_tags(username=username, is_owner=is_owner, tags=tag_array, ids=ids)[:30];
  tag_browse = True;
  paginator = Paginator(bookmarks, ITEMS_PER_PAGE);
  page = 1;
  if request.GET.has_key('page'):
    page = int(request.GET['page']);
  try:
    p = paginator.page(page);
  except:
    raise Http404;
  tag_nav = [];
  url = "/bookmarks/user/" + username + "/";
  for tag in tag_array:
    url += tag + "/";
    tag_dict = {'name': tag, 'url': url};
    tag_nav.append(tag_dict);
  variables = RequestContext(request, {
		'script_name':request.META['SCRIPT_NAME'],
    'page_type':'user',
    'content_type':'user',
    'sortedby':sortedby,
    'is_owner': is_owner,
    'user': request.user,
    'username':username,
    'bookmarks':p.object_list,
    'total':len(bookmarks),
    'tags':tags,
    'tag_nav':tag_nav,
    'show_edit':show_edit,
    'show_delete':show_delete,
    'show_save':show_save,
    'http_host':http_host,
    'tag_browse':tag_browse,
    'has_other_pages': p.has_other_pages(),
    'has_next': p.has_next(),
    'has_previous': p.has_previous(),
    'page': p.number,
    'pages': range(1, p.paginator.num_pages + 1),
    'next_page_number': p.next_page_number(),
    'previous_page_number': p.previous_page_number()
  })
  return render_to_response('bookmarks/bookmarks_page.html', variables)

# Add Bookmark
def add_bookmark(request):
  logging.debug("bookmarks.views.add_bookmark()");
  if not request.user.is_authenticated():
     url = request.path + '?' + request.META['QUERY_STRING'];
     url = urllib.quote(url);
     return HttpResponseRedirect('%s/accounts/login/?next=%s' % (request.META['SCRIPT_NAME'],url));
  if(request.GET.has_key('url') and request.GET.has_key('title')):
     # url
     url   = request.GET['url'];
     #title
     title = request.GET['title'];
     title = title.replace('\n', '');
     title = title.strip();
     notes = None;
     if request.GET.has_key('notes'):
       notes = request.GET['notes'];
     form  = BookmarkSaveForm({'url':url,'title':title,'notes':notes, 'share':True});
  else:
     form = BookmarkSaveForm(initial={'share':True});
  popup = False;
  if(request.GET.has_key('_popup')):
     popup = bool(request.GET['_popup']);
  variables = RequestContext(request, {
		'script_name':request.META['SCRIPT_NAME'],
     'user': request.user,
     'username':request.user.username,
     'form':form
  });
  if popup:
     return render_to_response('bookmarks/popup_save_page.html', variables);
  else:
    return render_to_response('bookmarks/save_page.html', variables);

# Copy Bookmark
def copy_bookmark(request, link_id):
  logging.debug("bookmarks.views.copy_bookmark() link_id=%s" % (link_id));
  if not request.user.is_authenticated():
    return HttpResponseRedirect('%s/accounts/login/?next=%s' % (request.META['SCRIPT_NAME'],request.path))
  link     = get_object_or_404(Link, id=link_id)
  try:
    bookmark = Bookmark.objects.get(link=link, user=request.user);
    return edit_bookmark(request, bookmark.id);
  except ObjectDoesNotExist:
    pass;
  url      = link.url;
  title    = link.title
  notes = None;
  form  = BookmarkSaveForm({'url':url,'title':title,'notes':notes, 'share':True});
  variables = RequestContext(request, {
		'script_name':request.META['SCRIPT_NAME'],
     'user': request.user,
     'username':request.user.username,
     'form':form
  });
  return render_to_response('bookmarks/save_page.html', variables);

# Edit Bookmark
def edit_bookmark(request, bookmark_id):
  logging.debug("bookmarks.views.edit_bookmark() bookmark_id=%s" % (bookmark_id));
  if not request.user.is_authenticated():
    return HttpResponseRedirect('%s/accounts/login/?next=%s' % (request.META['SCRIPT_NAME'],request.path))
  bookmark = get_object_or_404(Bookmark, id=bookmark_id)
  url      = bookmark.link.url
  title    = bookmark.title
  tags     = ' '.join(tag.name for tag in bookmark.tags.all())
  notes    = bookmark.notes
  share    = bookmark.share;
  form     = BookmarkSaveForm({'url':url,'title':title,'tags':tags, 'notes':notes, 'share':share})
  variables = RequestContext(request, {
		'script_name':request.META['SCRIPT_NAME'],
		'form':form})
  return render_to_response('bookmarks/save_page.html', variables)

# Delete Bookmark
def delete_bookmark(request, bookmark_id):
  logging.debug("bookmarks.views.delete_bookmark() bookmark_id=%s" % (bookmark_id));
  if not request.user.is_authenticated():
    return HttpResponseRedirect('%s/accounts/login/?next=%s' % (request.META['SCRIPT_NAME'],request.path))
  bookmark = get_object_or_404(Bookmark, id=bookmark_id)
  if(bookmark.user.username == request.user.username):
    link = bookmark.link;
    bookmark.delete();
    if(link.bookmark_set.count() == 0):
      link.delete();
  return HttpResponseRedirect('%s/bookmarks/user/%s' % (request.META['SCRIPT_NAME'],request.user.username))

# Save Bookmark
def save_bookmark(request):
  logging.debug("bookmarks.views.save_bookmark()");
  if not request.user.is_authenticated():
    return HttpResponseRedirect('%s/accounts/login/?next=%s' % (request.META['SCRIPT_NAME'],request.path))
  popup = False;
  if request.method == 'POST':
    if(request.POST.has_key('_popup')):
      popup = bool(request.POST['_popup']);
    form = BookmarkSaveForm(request.POST)
    if form.is_valid():
      bookmark = _save_bookmark(request, form)
      if(popup):
        return render_to_response('bookmarks/close_page.html')
      else:
        return HttpResponseRedirect('%s/bookmarks/user/%s' % (request.META['SCRIPT_NAME'],request.user.username))
  else:
    if(request.GET.has_key('_popup')):
      popup = bool(request.GET['_popup']);
  tags = Bookmark.objects.tag_clouds(request.user.username, True);
  variables = RequestContext(request, {
		'script_name':request.META['SCRIPT_NAME'],
    'user': request.user,
    'username':request.user.username,
    'form':form,
    'tags':tags
    });
  if(popup):
    return render_to_response('bookmarks/popup_save_page.html', variables)
  else:
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
  bookmark.save();
  return bookmark;

def search_bookmarks(request, username):
  logging.debug("bookmarks.views.search_bookmarks() username=%s" % (username));
  http_host = request.META['HTTP_HOST']
  user = get_object_or_404(User, username=username)
  if(user.username == request.user.username):
    is_owner    = True;    
    show_edit   = True;
    show_delete = True;
  else:
    is_owner    = False;    
    show_edit   = False;
    show_delete = False;
  tags = Bookmark.objects.tag_clouds(username, is_owner)[:10];
  keywords  = [];
  bookmarks = [];
  query = "";
  if request.GET.has_key('query'):
    query = request.GET['query'].strip();
    if query:
      keywords = query.split();
      q = Q();
      bookmarks = Bookmark.objects.filter(user=user);
      if not is_owner:
        bookmarks = bookmarks.filter(share=True);
      for keyword in keywords:
        q = Q(title__icontains=keyword) | Q(notes__icontains=keyword) | Q(link__url__icontains=keyword) | Q(tags__name__icontains=keyword);
        bookmarks = bookmarks.filter(q);
      bookmarks = bookmarks.distinct();
      bookmarks = bookmarks.order_by('-date');
  variables = RequestContext(request,{
		'script_name':request.META['SCRIPT_NAME'],
    'page_type':'search',
    'content_type':'user',
    'query':query,
    'user': request.user,
    'username': username,
    'bookmarks':bookmarks,
    'total':len(bookmarks),
    'tags':tags,
    'http_host':http_host,
    'is_owner': is_owner,
    'show_edit':show_edit,
    'show_delete':show_delete
    });
  return render_to_response('bookmarks/bookmarks_page.html', variables)

def public_search_bookmarks(request):
  logging.debug("bookmarks.views.public_search_bookmarks()");
  http_host = request.META['HTTP_HOST']
  tags  = Link.objects.tag_clouds(30);
  keywords  = [];
  links = [];
  query = "";
  if request.GET.has_key('query'):
    query = request.GET['query'].strip();
    if query:
      keywords = query.split();
      links = Link.objects.all();
      links = links.filter(Q(bookmark__share=True));
      for keyword in keywords:
        q = Q(title__icontains=keyword) | Q(url__icontains=keyword)|Q(bookmark__notes__icontains=keyword)|Q(bookmark__tags__name__icontains=keyword);
        links = links.filter(q);
      links = links.distinct();
  variables = RequestContext(request, {
		'script_name':request.META['SCRIPT_NAME'],
    'page_type':'search',
    'content_type':'public',
    'query':query,
    'links':links,
    'tags':tags,
    'http_host':http_host
  })
  return render_to_response('bookmarks/bookmarks_page.html', variables)
