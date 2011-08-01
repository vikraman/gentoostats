
import utils

def pprint(title, object):
    # TODO: write a custom pretty printer here
    import pprint
    print title
    pprint.pprint(object)

def add_parser(subparsers):
    # TODO: add help and descriptions for all opts
    search_parser = subparsers.add_parser('search')
    search_parser.add_argument('-c', '--category')
    search_parser.add_argument('-p', '--package')
    search_parser.add_argument('-v', '--version')
    search_parser.add_argument('-r', '--repo')
    search_parser.add_argument('--min_hosts', type=int)
    search_parser.add_argument('--max_hosts', type=int)
    search_parser.set_defaults(func=search)

def search(args):
    url_base = '/search'
    url_extra = ''

    url_extra += ('?', '&')[bool(url_extra)] + 'cat=' + args.category if args.category else ''
    url_extra += ('?', '&')[bool(url_extra)] + 'pkg=' + args.package if args.package else ''
    url_extra += ('?', '&')[bool(url_extra)] + 'ver=' + args.version if args.version else ''
    url_extra += ('?', '&')[bool(url_extra)] + 'repo=' + args.repo if args.repo else ''
    url_extra += ('?', '&')[bool(url_extra)] + 'min_hosts=' + str(args.min_hosts) if args.min_hosts else ''
    url_extra += ('?', '&')[bool(url_extra)] + 'max_hosts=' + str(args.max_hosts) if args.max_hosts else ''

    get_data = utils.GET(server = args.server, url = args.url + url_base + url_extra, headers = utils.headers)
    data = utils.deserialize(get_data)

    pprint ('Search results', data)
