
from config import render, db

class Feature(object):
  def GET(self):
	feature_count = db.query('SELECT FEATURE,COUNT(UUID) AS HOSTS FROM HOST_FEATURES NATURAL JOIN FEATURES GROUP BY FEATURE')
	feature_data = dict()
	for t in feature_count:
	  feature_data[t['FEATURE']] = {'HOSTS':t['HOSTS']}
	return render.feature(feature_data)
