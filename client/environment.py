
import logging
import subprocess

class Environment(object):

  def __init__(self):
    try:
      p = subprocess.Popen(['emerge', '--info'], stdout=subprocess.PIPE)
      self.out = p.stdout.readlines()
    except OSError, e:
      fatal('Cannot run emerge --info')
      raise e

  def getVar(self, myvar):
    for line in self.out:
      if line.startswith(myvar):
	return line.strip()
    return ''
