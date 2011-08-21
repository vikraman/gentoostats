
import helpers
from config import render, db

class Keyword(object):
    def GET(self):
        keyword_count = db.query('SELECT KEYWORD,\
                COUNT(DISTINCT IPKEY) AS PACKAGES,\
                COUNT(DISTINCT UUID) AS HOSTS\
                FROM GLOBAL_KEYWORDS NATURAL JOIN KEYWORDS\
                NATURAL JOIN INSTALLED_PACKAGES GROUP BY KEYWORD')
        keyword_data = dict()
        for t in keyword_count:
            keyword_data[t['KEYWORD']] = {'HOSTS':t['HOSTS'], 'PACKAGES':t['PACKAGES']}
        if helpers.is_json_request():
            return helpers.serialize(keyword_data)
        else:
            # generate plot
            x_ticklabels = keyword_data.keys()
            y_values = [ keyword_data[k]['PACKAGES'] for k in x_ticklabels ]
            keyword_plot = helpers.barchart(title = 'Installed packages per keyword',
                    x_label = 'Keyword', y_label = 'Number of Packages',
                    x_ticklabels = x_ticklabels, y_values = y_values)
            return render.keyword(keyword_data, keyword_plot)
