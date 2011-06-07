
import re

# split package name into cpv
# based on pkgsplit code 
# in portage/versions.py

def pkgsplit(pkgname):
  cpv={}
  pkgsplit = pkgname.split('/',1)
  cpv['cat'] = pkgsplit[0]
  pv_re =re.compile(r'(?x)^(?P<pn>[\w\+][\w\+-]*?(?P<pn_inval>-(cvs\.)?(\d+)((\.\d+)*)([a-z]?)((_(pre|p|beta|alpha|rc)\d*)*)(-r(\d+))?)?)-(?P<ver>(cvs\.)?(\d+)((\.\d+)*)([a-z]?)((_(pre|p|beta|alpha|rc)\d*)*))(-r(?P<rev>\d+))?$')
  m = pv_re.match(pkgsplit[1])
  cpv['pkg'] = m.group('pkg')
  rev = m.group('rev')
  if rev is None:
 	cpv['ver'] = m.group('ver')
  else:
	cpv['ver'] = m.group('ver') + '-r' + rev
  return cpv

# get functions for index keys
# lookup key and insert if not found

def get_kwkey(db, keyword):
  db_keyword = db.select('keywords', vars={'keyword':keyword}, where='keyword=$keyword')
  if len(db_keyword):
	kwkey = db_keyword[0].kwkey
  else:
	kwkey = db.insert('keywords', keyword=keyword)
  return kwkey

def get_lkey(db, lang):
  db_lang = db.select('lang', vars={'lang':lang}, where='lang=$lang')
  if len(db_lang):
	lkey = db_lang[0].lkey
  else:
	lkey = db.insert('lang', lang=lang)
  return lkey

def get_fkey(db, feature):
  db_feature = db.select('features', vars={'feature':feature}, where='feature=$feature')
  if len(db_feature):
	fkey = db_feature[0].fkey
  else:
	fkey = db.insert('features', feature=feature)
  return fkey

def get_mkey(db, mirror):
  db_mirror = db.select('gentoo_mirrors', vars={'mirror':mirror}, where='mirror=$mirror')
  if len(db_mirror):
	mkey = db_mirror[0].mkey
  else:
	mkey = db.insert('gentoo_mirrors', mirror=mirror)
  return mkey

def get_ukey(db, useflag):
  db_useflag = db.select('useflags', vars={'useflag':useflag}, where='useflag=$useflag')
  if len(db_useflag):
	ukey = db_useflag[0].ukey
  else:
	ukey = db.insert('useflags', useflag=useflag)
  return ukey

def get_pkey(db, package):
  cpv = pkgsplit(package)
  db_package = db.select('packages', vars=cpv, where='cat=$cat and pkg=$pkg and ver=$ver')
  if len(db_package):
	pkey = db_package[0].pkey
  else:
	pkey = db.insert('packages', cat=cpv['cat'], pkg=cpv['pkg'], ver=cpv['ver'])
  return pkey

def get_rkey(db, repo):
  db_repo = db.select('repositories', vars={'repo':repo}, where='repo=$repo')
  if len(db_repo):
	rkey = db_repo[0].rkey
  else:
	rkey = db.insert('repositories', repo=repo)
  return rkey

