
import helpers
from config import render, db

class Profile(object):
    def GET(self):
        profile_count = db.select('ENV', what='PROFILE, COUNT(UUID) AS HOSTS', group='PROFILE')
        profile_data = dict()
        for t in profile_count:
            profile_data[t['PROFILE']] = {'HOSTS':t['HOSTS']}
        if helpers.is_json_request():
            return helpers.serialize(profile_data)
        else:
            return render.profile(profile_data)
