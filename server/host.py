
import web
import json
import helpers
import config
from config import render, db

class Host(object):

  def GET(self, str_uuid):
	if not helpers.is_uuid(str_uuid):
	  return config.notfound()

	uuid = helpers.uuidbin(str_uuid)
	hosts = db.select('HOSTS', vars={'uuid':uuid}, where='UUID=$uuid', what='UUID')
	if len(hosts) == 0:
	  return config.notfound()

	get_data = dict()
	get_data['UUID'] = str_uuid

	env = db.select('ENV', vars={'uuid':uuid}, where="UUID=$uuid")
	e = env[0]
	for var in ['PLATFORM','LASTSYNC','PROFILE','ARCH','CHOST','CFLAGS','CXXFLAGS','FFLAGS','LDFLAGS','MAKEOPTS','SYNC']:
	  get_data[var] = e[var]
	
	get_data['FEATURES'] = list()
	features = db.query('SELECT FEATURE FROM HOST_FEATURES NATURAL JOIN FEATURES WHERE UUID=$uuid', vars={'uuid':uuid})
	for f in features:
	  get_data['FEATURES'].append(f['FEATURE'])

	get_data['ACCEPT_KEYWORDS'] = list()
	keywords = db.query('SELECT KEYWORD FROM GLOBAL_KEYWORDS NATURAL JOIN KEYWORDS WHERE UUID=$uuid', vars={'uuid':uuid})
	for k in keywords:
	  get_data['ACCEPT_KEYWORDS'].append(k['KEYWORD'])
	
	get_data['USE'] = list()
	useflags = db.query('SELECT USEFLAG FROM GLOBAL_USEFLAGS NATURAL JOIN USEFLAGS WHERE UUID=$uuid', vars={'uuid':uuid})
	for u in useflags:
	  get_data['USE'].append(u['USEFLAG'])

	get_data['LANG'] = list()
	lang = db.query('SELECT LANG FROM HOST_LANG NATURAL JOIN LANG WHERE UUID=$uuid', vars={'uuid':uuid})
	for l in lang:
	  get_data['LANG'].append(l['LANG'])

	get_data['GENTOO_MIRRORS'] = list()
	mirrors = db.query('SELECT MIRROR FROM HOST_MIRRORS NATURAL JOIN GENTOO_MIRRORS WHERE UUID=$uuid', vars={'uuid':uuid})
	for m in mirrors:
	  get_data['GENTOO_MIRRORS'].append(m['MIRROR'])

	get_data['PACKAGES'] = dict()
	packages = db.query('SELECT CAT, PKG, VER FROM INSTALLED_PACKAGES NATURAL JOIN PACKAGES WHERE UUID=$uuid ORDER BY CAT, PKG, VER', vars={'uuid':uuid})
	for p in packages:
	  cpv = p['CAT'] + '/' + p['PKG'] + '-' + p['VER']
	  get_data['PACKAGES'][cpv] = dict()

	return render.host(get_data)

  def POST(self, str_uuid):
	post_data = json.JSONDecoder().decode(web.data())

	#TODO: Handle exceptions
	if post_data['PROTOCOL'] != 1:
	  return 'Unsupported protocol!'

	if post_data['AUTH']['UUID'] != str_uuid:
	  return 'Invalid uuid!'

	uuid = helpers.uuidbin(str_uuid)

	# Insert in hosts
	db_host = db.select('HOSTS', vars={'uuid':uuid}, where='UUID=$uuid')
	if len(db_host):
	  if post_data['AUTH']['PASSWD'] != db_host[0]['PASSWD']:
		return 'Wrong password!'
	  # This should delete all host entries from all tables
	  db.delete('HOSTS', vars={'uuid':uuid}, where='UUID=$uuid')
	db.insert('HOSTS', UUID=uuid, PASSWD=post_data['AUTH']['PASSWD'])

	# Insert in env
	db.insert('ENV', UUID=uuid, ARCH=post_data['ARCH'], CHOST=post_data['CHOST'], CFLAGS=post_data['CFLAGS'],
		CXXFLAGS=post_data['CXXFLAGS'], FFLAGS=post_data['FFLAGS'], LDFLAGS=post_data['LDFLAGS'],
		MAKEOPTS=post_data['MAKEOPTS'], SYNC=post_data['SYNC'], PLATFORM=post_data['PLATFORM'],
		PROFILE=post_data['PROFILE'], LASTSYNC=post_data['LASTSYNC'])

	# Insert in GLOBAL_KEYWORDS
	for keyword in post_data['ACCEPT_KEYWORDS']:
	  kwkey = helpers.get_kwkey(db, keyword)
	  db.insert('GLOBAL_KEYWORDS', UUID=uuid, KWKEY=kwkey)

	# Insert in HOST_LANG
	for lang in post_data['LANG']:
	  lkey = helpers.get_lkey(db, lang)
	  db.insert('HOST_LANG', UUID=uuid, LKEY=lkey)

	# Insert in HOST_FEATURES
	for feature in post_data['FEATURES']:
	  fkey = helpers.get_fkey(db, feature)
	  db.insert('HOST_FEATURES', UUID=uuid, FKEY=fkey)

	# Insert in HOST_MIRRORS
	for mirror in post_data['GENTOO_MIRRORS']:
	  mkey = helpers.get_mkey(db, mirror)
	  db.insert('HOST_MIRRORS', UUID=uuid, MKEY=mkey)

	# Insert in GLOBAL_USEFLAGS
	for useflag in post_data['USE']:
	  ukey = helpers.get_ukey(db, useflag)
	  db.insert('GLOBAL_USEFLAGS', UUID=uuid, UKEY=ukey)

	# Handle PACKAGES
	for package in post_data['PACKAGES'].keys():
	  pkey = helpers.get_pkey(db, package)
	  post_data_pkg = post_data['PACKAGES'][package]
	  kwkey = helpers.get_kwkey(db, post_data_pkg['KEYWORD'])
	  rkey  = helpers.get_rkey(db, post_data_pkg['REPO'])

	  # Insert in INSTALLED_PACKAGES
	  ipkey = db.insert('INSTALLED_PACKAGES', UUID=uuid, PKEY=pkey, BUILD_TIME=int(post_data_pkg['BUILD_TIME']),
	  	  COUNTER=post_data_pkg['COUNTER'], KWKEY=kwkey, RKEY=rkey, SIZE=post_data_pkg['SIZE'])

	  # Insert in PLUS_USEFLAGS
	  for useflag in post_data_pkg['USE']['PLUS']:
		ukey = helpers.get_ukey(db, useflag)
		db.insert('PLUS_USEFLAGS', IPKEY=ipkey, UKEY=ukey)

	  # Insert in MINUS_USEFLAGS
	  for useflag in post_data_pkg['USE']['MINUS']:
		ukey = helpers.get_ukey(db, useflag)
		db.insert('MINUS_USEFLAGS', IPKEY=ipkey, UKEY=ukey)

	  # Insert in UNSET_USEFLAGS
	  for useflag in post_data_pkg['USE']['UNSET']:
	  	ukey = helpers.get_ukey(db, useflag)
		db.insert('UNSET_USEFLAGS', IPKEY=ipkey, UKEY=ukey)

	return 'POST for ' + str_uuid + ' successful'
