
from gentoolkit.flag import *

class UseFlags:

  def getUseFlags (self, cpv):
    return get_flags (cpv, True)[1]
