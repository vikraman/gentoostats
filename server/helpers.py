
import uuid
import re

# check valid uuid

def is_uuid(uuid):
  regex = re.compile(r'^(\w{8})-(\w{4})-(\w{4})-(\w{4})-(\w{12})$')
  return regex.search(uuid)

# convert uuid string to raw bytes

def uuidbin(string):
  #TODO: string is not a valid uuid
  u = uuid.UUID(string)
  return u.bytes

# split package name into cpv
# based on pkgsplit code 
# in portage/versions.py

def pkgsplit(pkgname):
  cpv={}
  pkgsplit = pkgname.split('/',1)
  cpv['cat'] = pkgsplit[0]
  pv_re =re.compile(r'(?x)^(?P<pn>[\w\+][\w\+-]*?(?P<pn_inval>-(cvs\.)?(\d+)((\.\d+)*)([a-z]?)((_(pre|p|beta|alpha|rc)\d*)*)(-r(\d+))?)?)-(?P<ver>(cvs\.)?(\d+)((\.\d+)*)([a-z]?)((_(pre|p|beta|alpha|rc)\d*)*))(-r(?P<rev>\d+))?$')
  m = pv_re.match(pkgsplit[1])
  cpv['pkg'] = m.group('pn')
  rev = m.group('rev')
  if rev is None:
 	cpv['ver'] = m.group('ver')
  else:
	cpv['ver'] = m.group('ver') + '-r' + rev
  return cpv

# get functions for index keys
# lookup key and insert if not found

def get_kwkey(db, keyword):
  db_keyword = db.select('KEYWORDS', vars={'keyword':keyword}, where='KEYWORD=$keyword')
  if len(db_keyword):
	kwkey = db_keyword[0]['KWKEY']
  else:
	kwkey = db.insert('KEYWORDS', KEYWORD=keyword)
  return kwkey

def get_lkey(db, lang):
  db_lang = db.select('LANG', vars={'lang':lang}, where='LANG=$lang')
  if len(db_lang):
	lkey = db_lang[0]['LKEY']
  else:
	lkey = db.insert('LANG', LANG=lang)
  return lkey

def get_fkey(db, feature):
  db_feature = db.select('FEATURES', vars={'feature':feature}, where='FEATURE=$feature')
  if len(db_feature):
	fkey = db_feature[0]['FKEY']
  else:
	fkey = db.insert('FEATURES', FEATURE=feature)
  return fkey

def get_mkey(db, mirror):
  db_mirror = db.select('GENTOO_MIRRORS', vars={'mirror':mirror}, where='MIRROR=$mirror')
  if len(db_mirror):
	mkey = db_mirror[0]['MKEY']
  else:
	mkey = db.insert('GENTOO_MIRRORS', MIRROR=mirror)
  return mkey

def get_ukey(db, useflag):
  db_useflag = db.select('USEFLAGS', vars={'useflag':useflag}, where='USEFLAG=$useflag')
  if len(db_useflag):
	ukey = db_useflag[0]['UKEY']
  else:
	ukey = db.insert('USEFLAGS', USEFLAG=useflag)
  return ukey

def get_pkey(db, package):
  cpv = pkgsplit(package)
  db_package = db.select('PACKAGES', vars=cpv, where='CAT=$cat and PKG=$pkg and VER=$ver')
  if len(db_package):
	pkey = db_package[0]['PKEY']
  else:
	pkey = db.insert('PACKAGES', CAT=cpv['cat'], PKG=cpv['pkg'], VER=cpv['ver'])
  return pkey

def get_rkey(db, repo):
  db_repo = db.select('REPOSITORIES', vars={'repo':repo}, where='REPO=$repo')
  if len(db_repo):
	rkey = db_repo[0]['RKEY']
  else:
	rkey = db.insert('REPOSITORIES', REPO=repo)
  return rkey