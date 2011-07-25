
import web
import helpers
from config import render, db

class Package(object):
    def GET(self, *args):
        try:
            top = int(web.input(top="5").top)
        except ValueError:
            top = 5
        l = len(args)
        if l == 0:
            return self.__GET(top)
        elif l == 1:
            return self.__GET_C(top, args[0])
        elif l == 2:
            cpv = helpers.pkgsplit(args[0] + '/' + args[1])
            if cpv['ver'] == '':
                return self.__GET_CP(top, cpv['cat'], cpv['pkg'])
            else:
                return self.__GET_CPV(cpv['cat'], cpv['pkg'], cpv['ver'])
        else:
            return config.internalerror()

    def __GET(self, top):
        p_query = db.query('SELECT COUNT(DISTINCT UUID) AS HOST_COUNT, \
                COUNT(DISTINCT CAT) AS C_COUNT, \
                COUNT(DISTINCT CAT, PKG) AS CP_COUNT, \
                COUNT(DISTINCT CAT, PKG, VER) AS CPV_COUNT\
                FROM INSTALLED_PACKAGES RIGHT OUTER JOIN PACKAGES\
                ON INSTALLED_PACKAGES.PKEY = PACKAGES.PKEY')
        p_tuple = p_query[0]
        p_data = {
                'HOST_COUNT':p_tuple['HOST_COUNT'],
                'C_COUNT':p_tuple['C_COUNT'],
                'CP_COUNT':p_tuple['CP_COUNT'],
                'CPV_COUNT':p_tuple['CPV_COUNT'],
                'TOP_C':self.__top(top)
                }
        if helpers.is_json_request():
            return helpers.serialize(p_data)
        else:
            return render.package(p_data)

    def __GET_C(self, top, cat):
        p_query = db.query('SELECT COUNT(DISTINCT UUID) AS HOST_COUNT, \
                COUNT(DISTINCT CAT, PKG) AS CP_COUNT, \
                COUNT(DISTINCT CAT, PKG, VER) AS CPV_COUNT\
                FROM INSTALLED_PACKAGES RIGHT OUTER JOIN PACKAGES\
                ON INSTALLED_PACKAGES.PKEY = PACKAGES.PKEY\
                WHERE CAT=$cat', vars={'cat':cat})
        p_tuple = p_query[0]
        p_data = {
                'HOST_COUNT':p_tuple['HOST_COUNT'],
                'CP_COUNT':p_tuple['CP_COUNT'],
                'CPV_COUNT':p_tuple['CPV_COUNT'],
                'TOP_CP':self.__top(top, cat)
                }
        if helpers.is_json_request():
            return helpers.serialize(p_data)
        else:
            return render.package_c(cat, p_data)

    def __GET_CP(self, top, cat, pkg):
        p_query = db.query('SELECT COUNT(DISTINCT UUID) AS HOST_COUNT, \
                COUNT(DISTINCT CAT, PKG, VER) AS CPV_COUNT\
                FROM INSTALLED_PACKAGES RIGHT OUTER JOIN PACKAGES\
                ON INSTALLED_PACKAGES.PKEY = PACKAGES.PKEY\
                WHERE CAT=$cat AND PKG=$pkg', vars={'cat':cat, 'pkg':pkg})
        p_tuple = p_query[0]
        p_data = {
                'HOST_COUNT':p_tuple['HOST_COUNT'],
                'CPV_COUNT':p_tuple['CPV_COUNT'],
                'TOP_CPV':self.__top(top, cat, pkg)
                }
        if helpers.is_json_request():
            return helpers.serialize(p_data)
        else:
            return render.package_cp(cat, pkg, p_data)

    def __GET_CPV(self, cat, pkg, ver):
        p_query = db.query('SELECT COUNT(DISTINCT UUID) AS HOST_COUNT\
                FROM INSTALLED_PACKAGES RIGHT OUTER JOIN PACKAGES\
                ON INSTALLED_PACKAGES.PKEY = PACKAGES.PKEY\
                WHERE CAT=$cat AND PKG=$pkg AND VER=$ver', vars={'cat':cat, 'pkg':pkg, 'ver':ver})
        p_tuple = p_query[0]
        p_data = {
                'HOST_COUNT':p_tuple['HOST_COUNT'],
                }
        if helpers.is_json_request():
            return helpers.serialize(p_data)
        else:
            return render.package_cpv(cat, pkg, ver, p_data)

    def __top(self, count, *args):
        t_list = list()
        if len(args) == 0:
            tc_query = db.query('SELECT CAT, COUNT(DISTINCT UUID) AS HOST_COUNT\
                    FROM INSTALLED_PACKAGES RIGHT OUTER JOIN PACKAGES\
                    ON INSTALLED_PACKAGES.PKEY = PACKAGES.PKEY\
                    GROUP BY CAT\
                    ORDER BY HOST_COUNT DESC, CAT')
            for idx in range(0, count):
                try:
                    tc_tuple = tc_query[idx]
                    t_list.append({
                          'CAT':tc_tuple['CAT'],
                          'HOST_COUNT':tc_tuple['HOST_COUNT']
                          })
                except IndexError:
                    break

        elif len(args) == 1:
            tcp_query = db.query('SELECT CAT, PKG, COUNT(DISTINCT UUID) AS HOST_COUNT\
                    FROM INSTALLED_PACKAGES RIGHT OUTER JOIN PACKAGES\
                    ON INSTALLED_PACKAGES.PKEY = PACKAGES.PKEY\
                    WHERE CAT=$cat\
                    GROUP BY CAT, PKG\
                    ORDER BY HOST_COUNT DESC, CAT, PKG',
                    vars={'cat':args[0]})
            for idx in range(0, count):
                try:
                    tcp_tuple = tcp_query[idx]
                    t_list.append({
                          'CAT':tcp_tuple['CAT'],
                          'PKG':tcp_tuple['PKG'],
                          'HOST_COUNT':tcp_tuple['HOST_COUNT']
                          })
                except IndexError:
                    break

        elif len(args) == 2:
            tcpv_query = db.query('SELECT CAT, PKG, VER, COUNT(DISTINCT UUID) AS HOST_COUNT\
                  FROM INSTALLED_PACKAGES RIGHT OUTER JOIN PACKAGES\
                  ON INSTALLED_PACKAGES.PKEY = PACKAGES.PKEY\
                  WHERE CAT=$cat AND PKG=$pkg\
                  GROUP BY CAT, PKG, VER\
                  ORDER BY HOST_COUNT DESC, CAT, PKG, VER',
                  vars={'cat':args[0], 'pkg':args[1]})
            for idx in range(0, count):
                try:
                    tcpv_tuple = tcpv_query[idx]
                    t_list.append({
                          'CAT':tcpv_tuple['CAT'],
                          'PKG':tcpv_tuple['PKG'],
                          'VER':tcpv_tuple['VER'],
                          'HOST_COUNT':tcpv_tuple['HOST_COUNT']
                          })
                except IndexError:
                    break

        return t_list
