import portage

PORTDB = portage.db[portage.root]["porttree"].dbapi
VARDB = portage.db[portage.root]["vartree"].dbapi
