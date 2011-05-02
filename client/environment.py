
import logging
import portage

class Environment(object):

  def getVar(self, myvar):
    ret = portage.settings[myvar]
    return ret
