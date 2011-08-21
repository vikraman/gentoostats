
import pprint as pp
from gentoostats import utils

def pprint(title, object):
    """
    Pretty printer for the decoded json data
    """
    print title
    pp.pprint(object)

def add_parser(subparsers):
    """
    Setup argparse parsers
    """
    list_parser = subparsers.add_parser('list')
    list_subparsers = list_parser.add_subparsers()

    objects = {
            'arch': ['parser_arch', list_arch],
            'feature': ['parser_feature', list_feature],
            'lang': ['parser_lang', list_lang],
            'mirror': ['parser_mirror', list_mirror],
            'repo': ['parser_repo', list_repo],
            'package': ['parser_package', list_package],
            'use': ['parser_use', list_use]
            }
    for obj in objects.keys():
        parser = vars()[objects[obj][0]] = list_subparsers.add_parser(obj)
        parser.set_defaults(func=objects[obj][1])

    # need separate arguments for package
    parser = vars()[objects['package'][0]]
    parser.add_argument('-t', '--top', type=int)
    parser.add_argument('-c', '--category')
    parser.add_argument('-p', '--package')
    parser.add_argument('-v', '--version')

    # need separate arguments for use
    parser = vars()[objects['use'][0]]
    parser.add_argument('--use')

def list_arch(args):
    """
    /arch
    """
    data = list(args.server, args.url, '/arch', utils.headers)
    pprint('Arch', data)

def list_feature(args):
    """
    /feature
    """
    data = list(args.server, args.url, '/feature', utils.headers)
    pprint('Feature', data)

def list_lang(args):
    """
    /lang
    """
    data = list(args.server, args.url, '/lang', utils.headers)
    pprint('Lang', data)

def list_mirror(args):
    """
    /mirror
    """
    data = list(args.server, args.url, '/mirror', utils.headers)
    pprint('Mirror', data)

def list_repo(args):
    """
    /repo
    """
    data = list(args.server, args.url, '/repo', utils.headers)
    pprint('Repo', data)

def list_package(args):
    """
    /package
    """
    url_top = ''
    if args.top:
        url_top = '?top=' + str(args.top)

    title = 'Categories'
    url_pkg = '/package'
    if args.category:
        title = 'Category: ' + args.category
        url_pkg += '/' + args.category
        if args.package:
            title = 'Category-Package: ' + args.category + '/' + args.package
            url_pkg += '/' + args.package
            if args.version:
                title = 'Category-Package-Version: ' + args.category + '/' + args.package + '-' + args.version
                url_pkg += '-' + args.version

    data = list(args.server, args.url, url_pkg + url_top, utils.headers)
    pprint(title, data)

def list_use(args):
    """
    /use
    """
    url_use = '/use'
    title = 'Useflags'
    if args.use:
        title = 'Useflag: ' + args.use
        url_use += '/' + args.use

    data = list(args.server, args.url, url_use, utils.headers)
    pprint(title, data)


def list(server, url_base, url_extra, headers):
    """
    Get and decode json from url
    """
    get_data = utils.GET(server=server, url=url_base+url_extra, headers=headers)
    data = utils.deserialize(get_data)
    return data
