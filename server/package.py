
import helpers
from config import render, db

class Package(object):
  def GET(self, *args):
	l = len(args)
	if l == 0:
	  return self.__GET()
	elif l == 1:
	  return self.__GET_C(args[0])
	elif l == 2:
	  cpv = helpers.pkgsplit(args[0] + '/' + args[1])
	  if cpv['ver'] == '':
		return self.__GET_CP(cpv['cat'], cpv['pkg'])
	  else:
		return self.__GET_CPV(cpv['cat'], cpv['pkg'], cpv['ver'])
	else:
	  return config.internalerror()

  def __GET(self):
	pquery = db.query('SELECT COUNT(DISTINCT UUID) AS HOST_COUNT,\
		COUNT(DISTINCT CAT) AS C_COUNT,\
		COUNT(DISTINCT CAT,PKG) AS CP_COUNT,\
		COUNT(DISTINCT CAT,PKG,VER) AS CPV_COUNT\
		FROM INSTALLED_PACKAGES RIGHT OUTER JOIN PACKAGES\
		ON INSTALLED_PACKAGES.PKEY = PACKAGES.PKEY')
	t = pquery[0]
	pdata = {
		'HOST_COUNT':t['HOST_COUNT'],
		'C_COUNT':t['C_COUNT'],
		'CP_COUNT':t['CP_COUNT'],
		'CPV_COUNT':t['CPV_COUNT']
		}
	return render.package(pdata)

  def __GET_C(self, cat):
	pquery = db.query('SELECT COUNT(DISTINCT UUID) AS HOST_COUNT,\
		COUNT(DISTINCT CAT,PKG) AS CP_COUNT,\
		COUNT(DISTINCT CAT,PKG,VER) AS CPV_COUNT\
		FROM INSTALLED_PACKAGES RIGHT OUTER JOIN PACKAGES\
		ON INSTALLED_PACKAGES.PKEY = PACKAGES.PKEY\
		WHERE CAT=$cat', vars={'cat':cat})
	t = pquery[0]
	pdata = {
		'HOST_COUNT':t['HOST_COUNT'],
		'CP_COUNT':t['CP_COUNT'],
		'CPV_COUNT':t['CPV_COUNT']
		}
	return render.package_c(cat, pdata)

  def __GET_CP(self, cat, pkg):
	pquery = db.query('SELECT COUNT(DISTINCT UUID) AS HOST_COUNT,\
		COUNT(DISTINCT CAT,PKG,VER) AS CPV_COUNT\
		FROM INSTALLED_PACKAGES RIGHT OUTER JOIN PACKAGES\
		ON INSTALLED_PACKAGES.PKEY = PACKAGES.PKEY\
		WHERE CAT=$cat AND PKG=$pkg', vars={'cat':cat,'pkg':pkg})
	t = pquery[0]
	pdata = {
		'HOST_COUNT':t['HOST_COUNT'],
		'CPV_COUNT':t['CPV_COUNT']
		}
	return render.package_cp(cat, pkg, pdata)

  def __GET_CPV(self, cat, pkg, ver):
	pquery = db.query('SELECT COUNT(DISTINCT UUID) AS HOST_COUNT\
		FROM INSTALLED_PACKAGES RIGHT OUTER JOIN PACKAGES\
		ON INSTALLED_PACKAGES.PKEY = PACKAGES.PKEY\
		WHERE CAT=$cat AND PKG=$pkg AND VER=$ver', vars={'cat':cat,'pkg':pkg,'ver':ver})
	t = pquery[0]
	pdata = {
		'HOST_COUNT':t['HOST_COUNT'],
		}
	return render.package_cpv(cat, pkg, ver, pdata)
