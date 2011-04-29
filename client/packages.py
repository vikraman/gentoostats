
import logging
from dbapi import VARDB

class Packages:
  def getInstalledCPs (self):
    installed_cps = sorted (VARDB.cp_all ())
    return installed_cps

  def getInstalledCPVs (self):
    installed_cpvs = sorted (VARDB.cpv_all ())
    return installed_cpvs
