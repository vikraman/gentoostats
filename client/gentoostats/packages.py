
import portage
from gentoostats.dbapi import VARDB

class Packages(object):
    """
    A class encapsulating providers for reading installed packages from portage
    """

    def getInstalledCPs(self, sort=False):
        """
        Read installed packages as category/packagename
        """
        installed_cps = VARDB.cp_all()
        if sort:
            return sorted(installed_cps)
        return installed_cps

    def getInstalledCPVs(self, sort=False):
        """
        Read installed packages as category/packagename-version
        """
        installed_cpvs = VARDB.cpv_all()
        if sort:
            return sorted(installed_cpvs)
        return installed_cpvs
