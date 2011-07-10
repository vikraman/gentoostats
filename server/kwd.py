
from config import render, db

class Keyword(object):
    def GET(self):
        keyword_count = db.query('SELECT KEYWORD, COUNT(DISTINCT IPKEY) AS PACKAGES, COUNT(DISTINCT UUID) AS HOSTS FROM GLOBAL_KEYWORDS NATURAL JOIN KEYWORDS NATURAL JOIN INSTALLED_PACKAGES GROUP BY KEYWORD')
        keyword_data = dict()
        for t in keyword_count:
            keyword_data[t['KEYWORD']] = {'HOSTS':t['HOSTS'],'PACKAGES':t['PACKAGES']}
        return render.keyword(keyword_data)
