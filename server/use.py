
from config import render, db

class Use(object):
  def GET(self):
	use_count = db.query('SELECT USEFLAG,COUNT(UUID) AS HOSTS FROM GLOBAL_USEFLAGS NATURAL JOIN USEFLAGS GROUP BY USEFLAG')
	use_data = dict()
	for t in use_count:
	  use_data[t['USEFLAG']] = {'HOSTS':t['HOSTS']}
	return render.use(use_data)
