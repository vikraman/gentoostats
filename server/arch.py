
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
            # generate plot
            x_ticklabels = arch_data.keys()
            y_values = [ arch_data[a]['HOSTS'] for a in x_ticklabels ]
            arch_plot = helpers.barchart(title = 'Hosts per arch', x_label = 'Arch',
                    y_label = 'Number of Hosts', x_ticklabels = x_ticklabels,
                    y_values = y_values)
            return render.arch(arch_data, arch_plot)
