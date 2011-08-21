
import sys
import pprint
import ConfigParser
from gentoostats.environment import Environment
from gentoostats.packages import Packages
from gentoostats.metadata import Metadata

class Payload(object):
    """
    A class that encapsulates payload operations
    """

    def __init__(self, configfile):
        """
        Initialize the payload using the config file
        """
        self.config = ConfigParser.ConfigParser()
        if len(self.config.read(configfile)) == 0:
            sys.stderr.write('Cannot read ' + configfile)
            sys.exit(1)

        self.payload = dict()
        self.payload['PROTOCOL'] = 1
        self.update()

    def __masked(self, section, item):
        """
        Check the mask status of payload
        """
        try:
            return not self.config.getboolean(section, item)
        except ConfigParser.NoOptionError:
            return False
        except (ConfigParser.NoSectionError, ValueError):
            sys.stderr.write('Malformed payload config')
            sys.exit(1)

    def update(self):
        """
        Read and update the payload
        """
        env = Environment()
        self.payload['PLATFORM'] = 'Unknown' if self.__masked('ENV', 'PLATFORM') else env.getPlatform()
        self.payload['LASTSYNC'] = 'Unknown' if self.__masked('ENV', 'LASTSYNC') else env.getLastSync()
        self.payload['PROFILE'] = 'Unknown' if self.__masked('ENV', 'PROFILE') else env.getProfile()

        for var in ['ARCH', 'CHOST', 'CFLAGS', 'CXXFLAGS', 'FFLAGS', 'LDFLAGS', 'MAKEOPTS', 'SYNC']:
            self.payload[var] = None if self.__masked('ENV', var) else env.getVar(var)

        for var in ['ACCEPT_KEYWORDS', 'LANG', 'GENTOO_MIRRORS', 'FEATURES', 'USE']:
            self.payload[var] = [] if self.__masked('ENV', var) else env.getVar(var).split()

        self.payload['PACKAGES'] = dict()
        for cpv in Packages().getInstalledCPVs():
            m = Metadata(cpv)
            p = dict()
            p['REPO'] = None if self.__masked('PACKAGES', 'REPO') else m.getRepoName()
            p['KEYWORD'] = None if self.__masked('PACKAGES', 'KEYWORD') else m.getKeyword()
            p['USE'] = dict()
            p['USE']['PLUS'] = [] if self.__masked('PACKAGES', 'USE_PLUS') else m.getPlusFlags()
            p['USE']['MINUS'] = [] if self.__masked('PACKAGES', 'USE_MINUS') else m.getMinusFlags()
            p['USE']['UNSET'] = [] if self.__masked('PACKAGES', 'USE_UNSET') else m.getUnsetFlags()
            p['COUNTER'] = None if self.__masked('PACKAGES', 'COUNTER') else m.getCounter()
            p['SIZE'] = None if self.__masked('PACKAGES', 'SIZE') else m.getSize()
            p['BUILD_TIME'] = None if self.__masked('PACKAGES', 'BUILD_TIME') else m.getBuildTime()
            self.payload['PACKAGES'][cpv] = p

    def get(self):
        """
        Return currently read payload
        """
        return self.payload

    def dump(self, human=False):
        """
        Dump payload
        """
        if human:
            pprint.pprint(self.payload)
        else:
            print self.payload
