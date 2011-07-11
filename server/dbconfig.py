
import sys
import ConfigParser

class DBConfig(object):

    def __init__(self, configfile):
        self.config = ConfigParser.ConfigParser()
        if len(self.config.read(configfile)) == 0:
            sys.stderr.write('Cannot read ' + configfile)
            sys.exit(1)

    def get_config(self):
        ret = dict()
        try:
            ret['DB'] = self.config.get('MYSQL', 'DB')
            ret['USER'] = self.config.get('MYSQL', 'USER')
            ret['PASS'] = self.config.get('MYSQL', 'PASS')

        except ConfigParser.NoSectionError, ConfigParser.NoOptionError:
            sys.stderr.write('Invalid db config')
            sys.exit(1)

        return ret
