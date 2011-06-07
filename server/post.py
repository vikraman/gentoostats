#!/usr/bin/env python

from helpers import *

def handler(uuid_str, data, db):
  #TODO: Handle exceptions
  if data['PROTOCOL'] != 1:
    return 'Unsupported protocol!'

  if data['AUTH']['UUID'] != uuid_str:
    return 'Invalid uuid!'

  uuid = uuidbin(uuid_str)

  # Insert in hosts
  db_host = db.select('hosts', vars={'uuid':uuid}, where='uuid=$uuid')
  if len(db_host):
    if data['AUTH']['PASSWD'] != db_host[0].passwd:
 	  return 'Wrong password!'
	# This should delete all host entries from all tables
    db.delete('hosts', vars={'uuid':uuid}, where='uuid=$uuid')
  db.insert('hosts', uuid=uuid, passwd=data['AUTH']['PASSWD'])

  # Insert in env
  db.insert('env', uuid=uuid, arch=data['ARCH'], chost=data['CHOST'], cflags=data['CFLAGS'],
	  cxxflags=data['CXXFLAGS'], fflags=data['FFLAGS'], ldflags=data['LDFLAGS'],
	  makeopts=data['MAKEOPTS'], sync=data['SYNC'], platform=data['PLATFORM'],
	  profile=data['PROFILE'], lastsync=data['LASTSYNC'])

  # Insert in global_keywords
  for keyword in data['ACCEPT_KEYWORDS']:
	kwkey = get_kwkey(db, keyword)
	db.insert('global_keywords', uuid=uuid, kwkey=kwkey)

  # Insert in host_lang
  for lang in data['LANG']:
	lkey = get_lkey(db, lang)
	db.insert('host_lang', uuid=uuid, lkey=lkey)

  # Insert in host_features
  for feature in data['FEATURES']:
	fkey = get_fkey(db, feature)
	db.insert('host_features', uuid=uuid, fkey=fkey)

  # Insert in host_mirrors
  for mirror in data['GENTOO_MIRRORS']:
	mkey = get_mkey(db, mirror)
	db.insert('host_mirrors', uuid=uuid, mkey=mkey)

  # Insert in global_useflags
  for useflag in data['USE']:
	ukey = get_ukey(db, useflag)
	db.insert('global_useflags', uuid=uuid, ukey=ukey)

  # Handle packages
  for package in data['PACKAGES'].keys():
	pkey = get_pkey(db, package)
	data_pkg = data['PACKAGES'][package]
  	kwkey = get_kwkey(db, data_pkg['KEYWORD'])
	rkey  = get_rkey(db, data_pkg['REPO'])
	
	# Insert in installed_packages
	ipkey = db.insert('installed_packages', uuid=uuid, pkey=pkey, build_time=data_pkg['BUILD_TIME'],
		counter=data_pkg['COUNTER'], kwkey=kwkey, rkey=rkey, size=data_pkg['SIZE'])

	# Insert in plus_useflags
	for useflag in data_pkg['USE']['PLUS']:
	  ukey = get_ukey(db, useflag)
	  db.insert('plus_useflags', ipkey=ipkey, ukey=ukey)
	
	# Insert in minus_useflags
	for useflag in data_pkg['USE']['MINUS']:
	  ukey = get_ukey(db, useflag)
	  db.insert('minus_useflags', ipkey=ipkey, ukey=ukey)

	# Insert in unset_useflags
	for useflag in data_pkg['USE']['UNSET']:
	  ukey = get_ukey(db, useflag)
	  db.insert('unset_useflags', ipkey=ipkey, ukey=ukey)

  return 'POST for ' + uuid_str + ' successful'
