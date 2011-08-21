
import web

class About(object):

    def GET(self):
        """
        Redirect to static about page
        """
        raise web.seeother('/static/about.html')
