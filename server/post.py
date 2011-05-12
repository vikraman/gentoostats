#!/usr/bin/env python

import re

def pkgsplit(pkgname):
  #TODO: Improve this
  cpv={}
  pkgsplit = pkgname.split('/',1)
  cpv['cat'] = pkgsplit[0]

  pv_re =re.compile(r'(?x)^(?P<pn>[\w\+][\w\+-]*?(?P<pn_inval>-(cvs\.)?(\d+)((\.\d+)*)([a-z]?)((_(pre|p|beta|alpha|rc)\d*)*)(-r(\d+))?)?)-(?P<ver>(cvs\.)?(\d+)((\.\d+)*)([a-z]?)((_(pre|p|beta|alpha|rc)\d*)*))(-r(?P<rev>\d+))?$')
  m = pv_re.match(pkgsplit[1])
  cpv['pn'] = m.group('pn')
  rev = m.group('rev')
  if rev is None:
    cpv['ver'] = m.group('ver')
  else:
    cpv['ver'] = m.group('ver') + '-r' + rev

  return cpv

def handler(uuid, data, db):
  #TODO: Handle exceptions
  if data['PROTOCOL'] != 1:
    return 'Unsupported protocol!'

  if data['AUTH']['UUID'] != uuid:
    return 'Invalid uuid!'

  host = db.select('hosts', vars={'uuid':uuid}, where='uuid=$uuid')
  if len(host):
    if data['AUTH']['PASSWD'] == host[0].passwd:
      exists = True
    else:
      return 'Wrong password!'
  else:
    db.insert('hosts', uuid=uuid, passwd=data['AUTH']['PASSWD'])
    exists = False

  if exists:
    db.delete('env', vars={'uuid':uuid}, where='uuid=$uuid')
  
  for var in ['CFLAGS', 'CXXFLAGS', 'LDFLAGS', 'CHOST', 'FEATURES']:
    db.insert('env', uuid=uuid, var=var, value=data[var])

  if exists:
    db.delete('useflags', vars={'uuid':uuid}, where='uuid=$uuid')

  pkg = data['PACKAGES']
  for cpv in pkg.keys():
    t = pkgsplit(cpv)
    s = db.select('packages', vars={'cat':t['cat'], 'pkg':t['pn'], 'ver':t['ver']},
	where='cat=$cat and pkg=$pkg and ver=$ver')
    if len(s) == 0:
      pkey = db.insert('packages', cat=t['cat'], pkg=t['pn'], ver=t['ver'])
    else:
      pkey = s[0].pkey
    for use in pkg[cpv]:
      db.insert('useflags', uuid=uuid, useflag=use, pkey=str(pkey))
  
  return 'POST for ' + uuid + ' successful'
