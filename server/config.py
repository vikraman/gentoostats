
import web

db = web.database(
	dbn='mysql',
	user='gentoo',
	pw='gentoo',
	db='gentoostats'
	)

render = web.template.render('templates/', base='layout')

def notfound():
  return web.notfound(render.error_404())

def internalerror():
  return web.internalerror(render.error_500())

