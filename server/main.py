#!/usr/bin/env python

import web
import config
from config import render
import json

urls = (
  r'/', 'index',
  r'/(.+)', 'stats'
)

class index:
  def GET(self):
    return render.index()

class stats:
  def GET(self, uuid):
    return '<html><body>GET success</body></html>'

  def POST(self, uuid):
    pdata = json.JSONDecoder().decode(web.data())
    print pdata
    return 'Post for ' + uuid + ' successful'

def notfound():
  return web.notfound(render.error_404())

def internalerror():
  return web.internalerror(render.error_500())

app = web.application(urls, globals())

app.notfound = notfound
app.internalerror = internalerror

if __name__ == "__main__":
  app.run()

