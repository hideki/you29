import logging
import urllib
import urllib2
from urllib import quote_plus
# Django includes simplejson. Use django's simplejson.
import django.utils.simplejson as simplejson
from you29.conf.ysearchconf import CONFIG

# configuration file -> conf/ysearch.conf

#CONFIG        = simplejson.load(open("you29/conf/ysearch.conf", "r"))
HEADERS        = {"User-Agent": CONFIG["agent"]}
SEARCH_API_URL = CONFIG["uri"].rstrip("/") + "/%s/v%d/%s?start=%d&count=%d&lang=%s&region=%s" + "&appid=" + CONFIG["appid"]

def download(url):
    logging.debug("download() url="+url);
    url = url.encode('utf-8');
    try:
        logging.debug('urlopen');
        o = urllib.urlopen(url)
        logging.debug('read');
        r = o.read();
        logging.debug("c");
        if all(map(lambda t: r.find(t) > 1, ["</head>", "</body>", "</html>"])):
            raise Error, "Why is this an html response?"
        logging.debug("OK: " + r);
        return r
    except:
        logging.debug("ERR");
        req = urllib2.Request(url, None, HEADERS)
        return urllib2.urlopen(req).read()

def load_json(url):
    logging.debug("load_json() url="+url);
    return simplejson.loads(download(url));

def params(d):
    p = "";
    for k, v in d.iteritems():
        p += "&%s=%s" % (quote_plus(k), quote_plus(v))
    return p

def search(command, vertical="web", version=1, start=0, count=10, lang="en", region="us", more={}):
    logging.debug("search() command="+command);
    #command = command.strip();
    #command = command.replace(" ", "+");
    command_list = command.split();
    command = "+".join(command_list);
    #url = SEARCH_API_URL % (vertical, version, quote_plus(command), start, count, lang, region) + params(more);
    url = SEARCH_API_URL % (vertical, version, command, start, count, lang, region) + params(more);
    #url = SEARCH_API_URL % (vertical, version, urllib.urlencode(command), start, count, lang, region) + params(more);
    logging.debug("search() url="+url);
    return load_json(url);

def web_search(command, start=0, count=10, lang="en", region="us", more={}):
    return search(command, "web", 1, start, count, lang, region, more);

def image_search(command, start=0, count=10, lang="en", region="us", more={}):
    return search(command, "images", 1, start, count, lang, region, more);

def news_search(command, start=0, count=10, lang="en", region="us", more={}):
    return search(command, "news", 1, start, count, lang, region, more);
