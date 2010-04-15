"""Google search appliance interface

Peter Cicman, Divio 2009
Stefan Foulis, Divio 2010

More docs here:
    http://code.google.com/apis/searchappliance/documentation/52/index.html
"""

import urllib
import urllib2
from xml.etree import ElementTree
from django.contrib.sites.models import Site
from gsa.queryset import FakeQuerySet
from logging import getLogger
logger = getLogger('gsa')

class GSA(object):
    """http://0.0.0.0/search?q=findme
        &access=p&entqr=0
        &sort=date%3AD%3AL%3Ad1
        &ud=1&oe=UTF-8&ie=UTF-8
        &output=xml
        &client=default_frontend
        &site=mysite
    """
    def __init__(self, host=None):
        self.host = host
        self.data = {}
    
    def query(self, q, site=None, lr=None, num=10, output="xml", client="default_frontend", **kwargs):
        """Queries GSA with given attributes.
        
        Args:
            g: search phrase
            site: search in specific collection (string or list of strings)
            lr: force search in specific language
            num: number of returned results (max 100)
            output: default output from GSA
            client: default client frontend
            
            kwargs: any other query command (appended to url)
            
        
        Returns: GSAResult instance
        """
        self.data['q'] = q
        if site:
            if not isinstance(site, list):
                site = [site]
            self.data['site'] = "|".join(site)
        if lr:
            self.data['lr'] = lr
        
        self.data['num'] = str(num)
        
        
        self.data['output'] = output
        self.data['client'] = client
        
        if not 'ie' in kwargs:
            # input encoding (query)
            self.data['ie'] = "UTF-8"
            
        if not 'oe' in kwargs:
            # output encoding (result)
            self.data['oe'] = "UTF-8"
        
        if kwargs:
            self.data.update(kwargs)
        
        _data = ["%s=%s" % (key, urllib2.quote(unicode(value).encode('utf8'))) for key, value in self.data.items()]
        #_data = ["%s=%s" % (key, urllib2.quote(value)) for key, value in self.data.items()]
        
        url = "http://%(host)s/search?%(data)s" %{
            'host': self.host,
            'data': "&".join(_data)
        } 
        try:
            response = urllib2.urlopen(url)
        #except urllib2
        except Exception, e:
            import sys
            #from traceback import format_exception
            #trace_exc = '\n'.join(format_exception(*sys.exc_info()))
            
            current_site = Site.objects.get_current()
            subject = "GSA %s failed. (query: %s site: %s)" % (self.host, url, current_site)
            logger.error(subject, exc_info=sys.exc_info())
            return GSAEmptyResult()
        
        return GSAResult(response)
    

class GSAResult(object):
    def __init__(self, response):
        self._response_data = None
        self._tree = None
        self.response = response
    
    
    def get_response_data(self):
        if not self._response_data:
            self._response_data = self.response.read()
            #print self._response_data
        return self._response_data
    
    response_data = property(get_response_data)    
    
    def get_tree(self):
        if not self._tree:
            self._tree = ElementTree.XML(self.response_data)
        return self._tree
        
    tree = property(get_tree)
    
    def links(self):
        for element in self.tree.getiterator("R"):
            s = element.find("S").text or ""
            try:
                t = element.find("T").text
            except:
                t = ""
            yield element.find("U").text, t, s
    
    def as_queryset(self):
        queryset = FakeQuerySet(list(self.links()))
        return queryset
          
    def count(self):
        try:
            return int(self.tree.find("./RES/M").text)
        except AttributeError:
            return 0
    
    __unicode__ = lambda self: self.response_data    


class GSAEmptyResult(GSAResult):
    def __init__(self):
        super(GSAEmptyResult, self).__init__("")
    
    def get_response_data(self):
        return ""
    
    response_data = property(get_response_data)    
            
    def links(self):
        return []
            
    def count(self):
        return 0
    
    __unicode__ = lambda self: self.response_data
    