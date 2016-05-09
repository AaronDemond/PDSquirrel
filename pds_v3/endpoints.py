__author__ = 'Aaron'

from ajax.exceptions import AJAXError

def example(request):
    if len(request.POST):
        return request.POST
    else:
        raise AJAXError(500, 'Nothing to echo back')
