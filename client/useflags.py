
#TODO: Remove gentoolkit dependency
from gentoolkit import flag

class UseFlags(object):

  def getUseFlags(self, cpv):
    return flag.get_flags(cpv, True)[1]
