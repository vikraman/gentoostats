
import sys
import json
import httplib

objects={
'arch':'list_arch',
'feature':'list_feature',
'lang':'list_lang',
'mirror':'list_mirror',
'repo':'list_repo',
'category':'list_cat',
}

server = 'soc.dev.gentoo.org'
url = '/gentoostats'
headers = {'Accept':'application/json'}

def print_usage():
    print 'Usage: list <object>'
    print 'Available objects:'
    for obj in objects.keys():
        print obj

def pprint(object):
    import pprint
    pprint.pprint(object)

def main(opts):
    l = len(opts)
    if l == 0:
        print_usage()
        sys.exit(1)

    if opts[0] not in objects:
        sys.stderr.write('Unknown object')
        sys.exit(1)

    try:
        globals()[objects[opts[0]]]()
    except KeyError:
        sys.stderr.write('Unimplemented')
        sys.exit(1)

def list_arch():
    conn = httplib.HTTPSConnection(server)
    conn.request('GET', url=url+'/arch', headers=headers)
    try:
        arch_data = json.JSONDecoder().decode(conn.getresponse().read())
    except ValueError:
        sys.exit(1)
    pprint(arch_data)

def list_feature():
    conn = httplib.HTTPSConnection(server)
    conn.request('GET', url=url+'/feature', headers=headers)
    try:
        feature_data = json.JSONDecoder().decode(conn.getresponse().read())
    except ValueError:
        sys.exit(1)
    pprint(feature_data)

def list_lang():
    conn = httplib.HTTPSConnection(server)
    conn.request('GET', url=url+'/lang', headers=headers)
    try:
        lang_data = json.JSONDecoder().decode(conn.getresponse().read())
    except ValueError:
        sys.exit(1)
    pprint(lang_data)

def list_mirror():
    conn = httplib.HTTPSConnection(server)
    conn.request('GET', url=url+'/mirror', headers=headers)
    try:
        mirror_data = json.JSONDecoder().decode(conn.getresponse().read())
    except ValueError:
        sys.exit(1)
    pprint(mirror_data)

def list_repo():
    conn = httplib.HTTPSConnection(server)
    conn.request('GET', url=url+'/mirror', headers=headers)
    try:
        repo_data = json.JSONDecoder().decode(conn.getresponse().read())
    except ValueError:
        sys.exit(1)
    pprint(repo_data)

def list_cat():
    conn = httplib.HTTPSConnection(server)
    conn.request('GET', url=url+'/package', headers=headers)
    try:
        cat_data = json.JSONDecoder().decode(conn.getresponse().read())
    except ValueError:
        sys.exit(1)
    pprint(cat_data)
