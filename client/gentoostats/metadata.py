
import portage
from gentoostats.dbapi import VARDB
from gentoolkit.enalyze.lib import FlagAnalyzer
from gentoolkit.enalyze.lib import KeywordAnalyser

class Metadata(object):
    """
    A class encapsulating all package metadata
    """

    def __init__(self, cpv):
        """
        Initialize the class with the cpv. All metadata are read from portage
        """
        self.repo, self.counter, self.build_time, self.size = VARDB.aux_get(cpv, ['repository', 'COUNTER', 'BUILD_TIME', 'SIZE'])

        system_use = portage.settings['USE'].split()
        fa = FlagAnalyzer(system=system_use)
        self.flags = fa.analyse_cpv(cpv)

        arch = portage.settings['ARCH']
        accept_keywords = portage.settings['ACCEPT_KEYWORDS'].split()
        ka = KeywordAnalyser(arch=arch, accept_keywords=accept_keywords)
        self.keyword = ka.get_inst_keyword_cpv(cpv)

    def getPlusFlags(self):
        """
        Return list of enabled useflags
        """
        return list(self.flags[0])

    def getMinusFlags(self):
        """
        Return list of disabled useflags
        """
        return list(self.flags[1])

    def getUnsetFlags(self):
        """
        Return list of unset useflags
        """
        return list(self.flags[2])

    def getKeyword(self):
        """
        Return keyword used to install package
        """
        return self.keyword

    def getRepoName(self):
        """
        Return the repository the package was installed from
        """
        if self.repo:
            return self.repo
        return 'Unknown'

    def getCounter(self):
        """
        Return the package install counter. How's this useful ?
        """
        return self.counter

    def getBuildTime(self):
        """
        Return the time package was built
        """
        return self.build_time

    def getSize(self):
        """
        Return the size of the installed package
        """
        return self.size
