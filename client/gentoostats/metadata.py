
import portage
from gentoostats.dbapi import VARDB
from gentoolkit.enalyze.lib import FlagAnalyzer
from gentoolkit.enalyze.lib import KeywordAnalyser

class Metadata(object):

    def __init__(self, cpv):
        self.repo, self.counter, self.build_time, self.size = VARDB.aux_get(cpv,['repository','COUNTER','BUILD_TIME','SIZE'])

        system_use = portage.settings['USE'].split()
        fa = FlagAnalyzer(system=system_use)
        self.flags = fa.analyse_cpv(cpv)

        arch = portage.settings['ARCH']
        accept_keywords = portage.settings['ACCEPT_KEYWORDS'].split()
        ka = KeywordAnalyser(arch=arch,accept_keywords=accept_keywords)
        self.keyword = ka.get_inst_keyword_cpv(cpv)

    def getPlusFlags(self):
        return list(self.flags[0])

    def getMinusFlags(self):
        return list(self.flags[1])

    def getUnsetFlags(self):
        return list(self.flags[2])

    def getKeyword(self):
        return self.keyword

    def getRepoName(self):
        if self.repo:
            return self.repo
        return 'Unknown'

    def getCounter(self):
        return self.counter

    def getBuildTime(self):
        return self.build_time

    def getSize(self):
        return self.size
