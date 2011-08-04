
import web

class About(object):

    def GET(self):
        raise web.seeother('/static/about.html')
