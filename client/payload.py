
import pprint
from environment import Environment
from packages import Packages
from metadata import Metadata

class Payload(object):

  def __init__(self):
    self.payload = dict()
    self.payload['PROTOCOL'] = 1
    self.update()

  def update(self):

    env = Environment()
    self.payload['PLATFORM'] = env.getPlatform()
    self.payload['LASTSYNC'] = env.getLastSync()
    self.payload['PROFILE'] = env.getProfile()

    for var in ['ARCH','CHOST','CFLAGS','CXXFLAGS','FFLAGS','LDFLAGS','MAKEOPTS','SYNC']:
      self.payload[var] = env.getVar(var)

    for var in ['ACCEPT_KEYWORDS','LANG','GENTOO_MIRRORS','FEATURES','USE']:
      self.payload[var] = env.getVar(var).split()

    self.payload['PACKAGES'] = dict()
    for cpv in Packages().getInstalledCPVs():
      m = Metadata(cpv)
      p = dict()
      p['REPO'] = m.getRepoName()
      p['KEYWORD'] = m.getKeyword()
      p['USE'] = dict()
      p['USE']['PLUS'] = m.getPlusFlags()
      p['USE']['MINUS'] = m.getMinusFlags()
      p['USE']['UNSET'] = m.getUnsetFlags()
      p['COUNTER'] = m.getCounter()
      p['SIZE'] = m.getSize()
      p['BUILD_TIME'] = m.getBuildTime()
      self.payload['PACKAGES'][cpv] = p

  def get(self):
    return self.payload

  def dump(self,human=False):
    if human:
      pprint.pprint(self.payload)
    else:
      print self.payload
