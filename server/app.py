#!/usr/bin/env python

import web
import config
from config import render
from index import Index
from arch import Arch
from profile import Profile
from mirror import Mirror
from feature import Feature
from kwd import Keyword
from use import Use
from repo import Repo
from lang import Lang
from package import Package
from host import Host
from search import Search
from about import About

urls = (
        r'', 'Index',
        r'/', 'Index',
        r'/arch', 'Arch',
        r'/profile', 'Profile',
        r'/mirror', 'Mirror',
        r'/feature', 'Feature',
        r'/keyword', 'Keyword',
        r'/repo', 'Repo',
        r'/lang', 'Lang',
        r'/package/(.+)/(.+)', 'Package',
        r'/package/(.+)', 'Package',
        r'/package', 'Package',
        r'/use/(.+)', 'Use',
        r'/use', 'Use',
        r'/host/(.+)', 'Host',
        r'/host', 'Host',
        r'/search', 'Search',
        r'/about', 'About'
        )

app = web.application(urls, globals(), autoreload=True)

app.notfound = config.notfound
app.internalerror = config.internalerror

if __name__ == "__main__":
    app.run()
