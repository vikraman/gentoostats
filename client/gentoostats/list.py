
import sys
import json
import httplib
import utils

objects = {
        'arch': 'list_arch',
        'feature': 'list_feature',
        'lang': 'list_lang',
        'mirror': 'list_mirror',
        'repo': 'list_repo',
        'cat': 'list_cat',
        'cp': 'list_cp',
        'cpv': 'list_cpv'
        }

server = 'soc.dev.gentoo.org'
url = '/gentoostats'
headers = {'Accept': 'application/json'}

def print_usage(objects):
    print 'Usage: list <object>'
    print 'Available objects:'
    for obj in objects.keys():
        print obj

def pprint(title, object):
    print title
    import pprint
    pprint.pprint(object)

def main(opts):
    l = len(opts)
    if l == 0:
        print_usage(objects)
        sys.exit(1)

    if opts[0] not in objects:
        sys.stderr.write('Unknown object')
        sys.exit(1)

    try:
        globals()[objects[opts[0]]](server, url, headers)
    except KeyError:
        sys.stderr.write('Unimplemented')
        sys.exit(1)

def list(server, url_base, url_extra, headers):
    get_data = utils.GET(server=server, url=url_base+url_extra, headers=headers)
    data = utils.deserialize(get_data)
    return data

def list_arch(server, url, headers):
    data = list(server, url, '/arch', headers)
    pprint('Arch', data)

def list_feature(server, url, headers):
    data = list(server, url, '/feature', headers)
    pprint('Feature', data)

def list_lang(server, url, headers):
    data = list(server, url, '/lang', headers)
    pprint('Lang', data)

def list_mirror(server, url, headers):
    data = list(server, url, '/mirror', headers)
    pprint('Mirror', data)

def list_repo(server, url, headers):
    data = list(server, url, '/repo', headers)
    pprint('Repo', data)

def list_cat(server, url, headers):
    data = list(server, url, '/package', headers)
    pprint('Category', data)

def list_cp(server, url, headers):
    data = list(server, url, '/package', headers)
    pprint('Category/Package', data)

def list_cpv(server, url, headers):
    data = list(server, url, '/package', headers)
    pprint('Category/Package-Version', data)
