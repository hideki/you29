import logging

from django.shortcuts import render_to_response
from django.template import RequestContext

from you29.utils.ysearch import image_search


# View for Image Search Page
def image_search_page(request):
    logging.debug("search.views.image_search_page");
    if(request.GET.has_key('query')):
      query = request.GET['query'];
      query = query.strip();
      logging.debug("query=" + query);
      if(len(query)):
        response = image_search(query, 0, 18);
        variables = RequestContext(request, {
          'query':query,
          'response':response['ysearchresponse']
        });
      else:
        variables = RequestContext(request, {});
    else:
      logging.debug("query=null" );
      variables = RequestContext(request, {});
    return render_to_response('search/image_search_page.html', variables);

