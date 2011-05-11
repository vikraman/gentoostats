#!/usr/bin/env python

import web
import config
import json
from config import render
from post import handler

urls = (
  r'/', 'index',
  r'/(.+)', 'stats'
)

db = web.database(
    dbn='mysql',
    user='vh4x0r',
    pw='vh4x0r',
    db='gentoostats'
    )

class index:
  def GET(self):
    hosts = db.select('hosts')
    return render.index(hosts)

class stats:
  def GET(self, uuid):
    if uuid == 'favicon.ico':
      return notfound()
    hosts = db.select('hosts', vars=locals(), where="uuid=$uuid")
    env = db.select('env', vars=locals(), where="uuid=$uuid")
    return render.stats(uuid, hosts, env)

  def POST(self, uuid):
    post_data = json.JSONDecoder().decode(web.data())
    return handler(uuid, post_data, db)

def notfound():
  return web.notfound(render.error_404())

def internalerror():
  return web.internalerror(render.error_500())

app = web.application(urls, globals())

app.notfound = notfound
app.internalerror = internalerror

if __name__ == "__main__":
  app.run()

