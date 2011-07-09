
from config import render, db

class Use(object):
  def GET(self, *args):
	l = len(args)
	if l == 0:
	  use_query = db.query('SELECT COUNT(DISTINCT UKEY) AS USE_COUNT FROM USEFLAGS')
	  use_tuple = use_query[0]
	  use_data = {'USE_COUNT':use_tuple['USE_COUNT']}
	  return render.use(use_data)

	elif l == 1:
	  global_use_query = db.query('SELECT COUNT(DISTINCT UUID) AS GLOBAL_COUNT\
		  FROM GLOBAL_USEFLAGS RIGHT OUTER JOIN USEFLAGS\
		  ON GLOBAL_USEFLAGS.UKEY = USEFLAGS.UKEY\
		  WHERE USEFLAG=$useflag', vars={'useflag':args[0]})
	  plus_use_query = db.query('SELECT COUNT(DISTINCT IPKEY) AS PLUS_COUNT\
		  FROM PLUS_USEFLAGS RIGHT OUTER JOIN USEFLAGS\
		  ON PLUS_USEFLAGS.UKEY = USEFLAGS.UKEY\
		  WHERE USEFLAG=$useflag', vars={'useflag':args[0]})
	  minus_use_query = db.query('SELECT COUNT(DISTINCT IPKEY) AS MINUS_COUNT\
		  FROM MINUS_USEFLAGS RIGHT OUTER JOIN USEFLAGS\
		  ON MINUS_USEFLAGS.UKEY = USEFLAGS.UKEY\
		  WHERE USEFLAG=$useflag', vars={'useflag':args[0]})
	  unset_use_query = db.query('SELECT COUNT(DISTINCT IPKEY) AS UNSET_COUNT\
		  FROM UNSET_USEFLAGS RIGHT OUTER JOIN USEFLAGS\
		  ON UNSET_USEFLAGS.UKEY = USEFLAGS.UKEY\
		  WHERE USEFLAG=$useflag', vars={'useflag':args[0]})
	  
	  global_use_tuple = global_use_query[0]
	  plus_use_tuple = plus_use_query[0]
	  minus_use_tuple = minus_use_query[0]
	  unset_use_tuple = unset_use_query[0]

	  use_data = {
		  'GLOBAL_COUNT':global_use_tuple['GLOBAL_COUNT'],
		  'PLUS_COUNT':plus_use_tuple['PLUS_COUNT'],
		  'MINUS_COUNT':minus_use_tuple['MINUS_COUNT'],
		  'UNSET_COUNT':unset_use_tuple['UNSET_COUNT']
		  }

	  return render.use_useflag(args[0], use_data)

	else:
	  return config.internalerror()
