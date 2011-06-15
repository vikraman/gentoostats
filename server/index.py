
from config import render, db

class Index(object):
  def GET(self):
  	hosts = db.select('HOSTS', what='COUNT(UUID) as COUNT')
	count = hosts[0]['COUNT']
	return render.index(count)
