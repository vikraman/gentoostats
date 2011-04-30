
import logging
from subprocess import *

class Environment:

  def __init__ (self):
    try:
      p = Popen (['emerge', '--info'], stdout=PIPE)
      self.out = p.stdout.readlines ()
    except OSError, e:
      fatal ('Cannot run emerge --info')
      raise e

  def getVar (self, myvar):
    for line in self.out:
      if line.startswith (myvar):
	return line.strip ()
    return ''
