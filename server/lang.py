
import helpers
from config import render, db

class Lang(object):
    def GET(self):
        lang_count = db.query('SELECT LANG,COUNT(UUID) AS HOSTS\
                FROM HOST_LANG NATURAL JOIN LANG GROUP BY LANG')
        lang_data = dict()
        for t in lang_count:
            lang_data[t['LANG']] = {'HOSTS':t['HOSTS']}
        if helpers.is_json_request():
            return helpers.serialize(lang_data)
        else:
            return render.lang(lang_data)
