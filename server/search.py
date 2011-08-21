
import web
import string
import helpers
from config import render, db

what = ['CAT', 'PKG', 'VER', 'REPO', 'COUNT(DISTINCT UUID) AS HOSTS']
order_by = ['HOSTS DESC','CAT', 'PKG', 'VER', 'REPO']
group_by = ['CAT', 'PKG', 'VER', 'REPO']
which = ['PACKAGES','INSTALLED_PACKAGES','REPOSITORIES']

class Search(object):

    def GET(self):
        self.args = web.input(cat='any', pkg='any', ver='any', repo='any')

        try:
            self.min_hosts = int(web.input(min_hosts=-1).min_hosts)
        except ValueError:
            self.min_hosts = -1

        try:
            self.max_hosts = int(web.input(max_hosts=-1).max_hosts)
        except ValueError:
            self.max_hosts = -1

        where = self._build_where()
        having = self._build_having()
        query = self._build_query(where, having)
        search_tuples = db.query(query, vars={
            'cat':self.args.cat,
            'pkg':self.args.pkg,
            'ver':self.args.ver,
            'repo':self.args.repo,
            'min_hosts':self.min_hosts,
            'max_hosts':self.max_hosts})
        if helpers.is_json_request():
            search_list = list()
            for tuple in search_tuples:
                search_list.append({
                    'CAT': tuple['CAT'],
                    'PKG': tuple['PKG'],
                    'VER': tuple['VER'],
                    'REPO': tuple['REPO'],
                    'HOSTS': tuple['HOSTS']
                    })
            return helpers.serialize(search_list)
        else:
            return render.search(search_tuples)

    def _build_query(self, where, having):
        """
        Build SELECT clause
        """
        sep = ' '
        query = ''
        query += 'SELECT' + sep + ','.join(what) + sep
        query += 'FROM' + sep + (sep + 'NATURAL LEFT OUTER JOIN' + sep).join(which) + sep
        if len(where) != 0:
            query += 'WHERE' + sep
            query += (sep + 'AND' + sep).join(where)
        query += sep
        query += 'GROUP BY' + sep + ','.join(group_by) + sep
        if len(having) != 0:
            query += 'HAVING' + sep
            query += (sep + 'AND' + sep).join(having)
        query += sep
        query += 'ORDER BY' + sep + ','.join(order_by) + sep
        return query.strip()

    def _build_where(self):
        """
        Build WHERE clause
        """
        where = []
        cat = string.lower(self.args.cat)
        if cat != 'any':
            where.append('CAT=$cat')

        pkg = string.lower(self.args.pkg)
        if pkg != 'any':
            where.append('PKG=$pkg')

        ver = string.lower(self.args.ver)
        if ver != 'any':
            where.append('VER=$ver')

        repo = string.lower(self.args.repo)
        if repo != 'any':
            where.append('REPO=$repo')
        return where

    def _build_having(self):
        """
        Build HAVING clause
        """
        having = []
        if self.min_hosts != -1:
            having.append('HOSTS>=$min_hosts')
        if self.max_hosts != -1:
            having.append('HOSTS<=$max_hosts')
        return having
