import re

page_re = re.compile(r'&page=\d*')

def no_page_query_string(request):
    """Returns query string without any &page=...
    """
    return page_re.sub('', request.META['QUERY_STRING'])
