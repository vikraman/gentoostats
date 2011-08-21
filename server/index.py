
from web import form
from config import render, db

# package search form
search_form = form.Form(
        form.Textbox('cat', value = 'any', description = 'Category'),
        form.Textbox('pkg', value = 'any', description = 'Package'),
        form.Textbox('ver', value = 'any', description = 'Version'),
        form.Textbox('repo', value = 'any', description = 'Repository'),
        form.Textbox('min_hosts', value = 'any', description = 'Minimum hosts'),
        form.Textbox('max_hosts', value = 'any', description = 'Maximum hosts'),
        form.Button('Search', type = 'submit')
        )

class Index(object):
    def GET(self):
        hosts = db.select('HOSTS', what='COUNT(UUID) as COUNT')
        count = hosts[0]['COUNT']

        form = search_form()

        return render.index(count, form)
