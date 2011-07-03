
from config import render, db

class Profile(object):
  def GET(self):
	profile_count = db.select('ENV', what='PROFILE, COUNT(UUID) AS HOSTS', group='PROFILE')
	profile_data = dict()
	for t in profile_count:
	  profile_data[t['PROFILE']] = {'HOSTS':t['HOSTS']}
	return render.profile(profile_data)
