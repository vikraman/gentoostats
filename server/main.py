#!/usr/bin/env python

import web
import config
from config import render
from index import Index
from host import Host

urls = (
	r'/', 'Index',
	r'/host/(.+)', 'Host'
	)

app = web.application(urls, globals())

app.notfound = config.notfound
app.internalerror = config.internalerror

if __name__ == "__main__":
  app.run()

