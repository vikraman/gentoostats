
import os
import sys
import web

db = web.database(
        dbn='mysql',
        user='gentoostats',
        pw='poicyurp3ZaddajGhaf',
        db='gentoostats'
        )

rootdir = os.path.abspath(os.path.dirname(__file__)) + '/'
render = web.template.render(rootdir + 'templates/', base='layout')

def notfound():
    return web.notfound(render.error_404())

def internalerror():
    return web.internalerror(render.error_500())
