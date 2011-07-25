
import helpers
from config import render, db

class Arch(object):
    def GET(self):
        arch_count = db.select('ENV', what='ARCH, COUNT(UUID) AS HOSTS', group='ARCH')
        arch_data = dict()
        for t in arch_count:
            arch_data[t['ARCH']] = {'HOSTS':t['HOSTS']}
        if helpers.is_json_request():
            return helpers.serialize(arch_data)
        else:
            return render.arch(arch_data)
