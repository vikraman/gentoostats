
import helpers
from config import render, db

class Mirror(object):
    def GET(self):
        mirror_count = db.query('SELECT MIRROR,COUNT(UUID) AS HOSTS\
                FROM HOST_MIRRORS NATURAL JOIN GENTOO_MIRRORS GROUP BY MIRROR')
        mirror_data = dict()
        for t in mirror_count:
            mirror_data[t['MIRROR']] = {'HOSTS':t['HOSTS']}
        if helpers.is_json_request():
            return helpers.serialize(mirror_data)
        else:
            return render.mirror(mirror_data)
