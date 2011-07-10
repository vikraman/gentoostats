
import logging
import portage
from gentoostats.dbapi import VARDB

class Packages(object):

    def getInstalledCPs(self, sort=False):
        installed_cps = VARDB.cp_all()
        if sort:
            return sorted(installed_cps)
        return installed_cps

    def getInstalledCPVs(self, sort=False):
        installed_cpvs = VARDB.cpv_all()
        if sort:
            return sorted(installed_cpvs)
        return installed_cpvs
