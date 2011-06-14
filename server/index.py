
from config import render, db

class Index(object):
  def GET(self):
  	hosts = db.select('hosts', what='count(uuid) as count')
	count = hosts[0].count
	return render.index(count)
