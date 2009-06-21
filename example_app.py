#!/usr/bin/env python

from mnml import TokenBasedApplication, RegexBasedApplication, \
                 RequestHandler, HttpError, HttpResponse, HttpResponseRedirect, \
                 development_server

# a MNML application consists of a series of RequestHandlers which return
# HttpResponse objects when methods are called. The method called should 
# match the HTTP method of the request.

class Foo(RequestHandler):
    "Demonstrates multiple methods and taking optional arguments"
    def GET(self, number=1, number2=1):
        """
        A get request which may provide two arguments, both of which have
        default values.
        """
        # If you wanted you could use a template engine of your choice
        # here as long as it can render to a string which
        # can be returned in the body of a HttpResponse
        return HttpResponse("<h1>Hello World of %s and %s</h1>" % 
            (number, number2)
        )

    def PUT(self):
        "A simple demonstration of a PUT method"
        return HttpResponse("<h1>Hello World of Put</h1>")

class Bar(RequestHandler):
    "A second handler, demonstrating different methods"
    def GET(self):
        "Demonstration of using a 301 redirect"
        return HttpResponseRedirect("/")

    def DELETE(self):
        "Demonstration of using a 302 redirect"
        return HttpResponseRedirect("/", False)

class RaisesException(RequestHandler):
    "A handler that throws a HTTP exception"
    def GET(self):
        raise HttpError(400)
    
class NotFoundPageHandler(RequestHandler):
    """
    Although the framework will capture page not found errors you
    might want to do that yourself so you have more control over
    what happends next
    """
    def GET(self):
        """
        Demonstration of using the build in error response.
        You'll probably want to overload that in some cases to 
        get even more control over procedings
        """
        return self.error(404)
            
# MNML supports two different routing mechanisms. One using regular
# expressions and another using tokens. This is done predominantly to
# highlight the pluggable nature of MNML, but also because the two
# authors both prefer different approaches. Use whichever suites you best.
            
routes = (
    (r'^/$', Foo),
    (r'^/foo/([0-9]+)/([0-9]+)', Foo),
    (r'^/bar$', Bar),
    (r'^/exception$', RaisesException),
    ('/.*', NotFoundPageHandler),
)
application = RegexBasedApplication(routes)

"""
routes = (
    ('/', Foo),
    ('/myview/:stuff/', Bar)
)
application = TokenBasedApplication(routes)
"""

if __name__ == '__main__':
    # run the MNML development server
    development_server(application)