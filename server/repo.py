
from config import render, db

class Repo(object):
  def GET(self):
	repo_count = db.query('select REPO,COUNT(DISTINCT IPKEY) AS PACKAGES,COUNT(DISTINCT UUID) AS HOSTS from INSTALLED_PACKAGES natural join REPOSITORIES group by REPO')
	repo_data = dict()
	for t in repo_count:
	  repo_data[t['REPO']] = {'HOSTS':t['HOSTS'], 'PACKAGES':t['PACKAGES']}
	return render.repo(repo_data)
