
import web
import json
import uuid
import re
import StringIO
import base64
from portage.versions import catpkgsplit

# matplotlib requires a writable home directory
import os
os.environ['HOME'] = '/tmp'
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

def is_uuid(uuid):
    """
    Check uuid validity
    """
    regex = re.compile(r'^(\w{8})-(\w{4})-(\w{4})-(\w{4})-(\w{12})$')
    return regex.search(uuid)

def uuidbin(string):
    """
    Convert uuid string to raw bytes
    """
    u = uuid.UUID(string)
    return u.bytes

def pkgsplit(pkgname):
    """
    Custom pkgsplit
    """
    cpv={'cat':'','pkg':'','ver':''}
    cpvr = catpkgsplit(pkgname)
    if cpvr is None:
        pkgsplit = pkgname.split('/')
        cpv['cat'] = pkgsplit[0]
        cpv['pkg'] = pkgsplit[1]
    else:
        cpv['cat'] = cpvr[0]
        cpv['pkg'] = cpvr[1]
        cpv['ver'] = cpvr[2]
        if cpvr[3] != 'r0':
            cpv['ver'] = cpv['ver'] + '-' + cpvr[3]
    return cpv

def get_kwkey(db, keyword):
    """
    Lookup keyword and return index key. Insert keyword if not found.
    """
    if keyword is None:
        return None
    db_keyword = db.select('KEYWORDS', vars={'keyword':keyword}, where='KEYWORD=$keyword')
    if len(db_keyword):
        kwkey = db_keyword[0]['KWKEY']
    else:
        kwkey = db.insert('KEYWORDS', KEYWORD=keyword)
    return kwkey

def get_lkey(db, lang):
    """
    Lookup lang and return index key. Insert lang if not found.
    """
    if lang is None:
        return None
    db_lang = db.select('LANG', vars={'lang':lang}, where='LANG=$lang')
    if len(db_lang):
        lkey = db_lang[0]['LKEY']
    else:
        lkey = db.insert('LANG', LANG=lang)
    return lkey

def get_fkey(db, feature):
    """
    Lookup feature and return index key. Insert feature if not found.
    """
    if feature is None:
        return None
    db_feature = db.select('FEATURES', vars={'feature':feature}, where='FEATURE=$feature')
    if len(db_feature):
        fkey = db_feature[0]['FKEY']
    else:
        fkey = db.insert('FEATURES', FEATURE=feature)
    return fkey

def get_mkey(db, mirror):
    """
    Lookup mirror and return index key. Insert mirror if not found.
    """
    if mirror is None:
        return None
    db_mirror = db.select('GENTOO_MIRRORS', vars={'mirror':mirror}, where='MIRROR=$mirror')
    if len(db_mirror):
        mkey = db_mirror[0]['MKEY']
    else:
        mkey = db.insert('GENTOO_MIRRORS', MIRROR=mirror)
    return mkey

def get_ukey(db, useflag):
    """
    Lookup useflag and return index key. Insert useflag if not found.
    """
    if useflag is None:
        return None
    db_useflag = db.select('USEFLAGS', vars={'useflag':useflag}, where='USEFLAG=$useflag')
    if len(db_useflag):
        ukey = db_useflag[0]['UKEY']
    else:
        ukey = db.insert('USEFLAGS', USEFLAG=useflag)
    return ukey

def get_pkey(db, package):
    """
    Lookup package and return index key. Insert package if not found.
    """
    if package is None:
        return None
    cpv = pkgsplit(package)
    db_package = db.select('PACKAGES', vars=cpv, where='CAT=$cat and PKG=$pkg and VER=$ver')
    if len(db_package):
        pkey = db_package[0]['PKEY']
    else:
        pkey = db.insert('PACKAGES', CAT=cpv['cat'], PKG=cpv['pkg'], VER=cpv['ver'])
    return pkey

def get_rkey(db, repo):
    """
    Lookup repo and return index key. Insert repo if not found.
    """
    if repo is None:
        return None
    db_repo = db.select('REPOSITORIES', vars={'repo':repo}, where='REPO=$repo')
    if len(db_repo):
        rkey = db_repo[0]['RKEY']
    else:
        rkey = db.insert('REPOSITORIES', REPO=repo)
    return rkey

def is_json_request():
    """
    Check for json headers
    """
    return web.ctx.environ['HTTP_ACCEPT'].find('json') != -1

def serialize(object, human=True):
    """
    Encode object in json
    """
    if human:
        indent = 2
    else:
        indent = None
    return json.JSONEncoder(indent=indent).encode(object)

def barchart(title, x_label, x_ticklabels, y_label, y_values):
    """
    Generate a barchart and return base64 encoded image data
    """
    fig = Figure()
    canvas = FigureCanvas(fig)
    ind = range(len(y_values))

    ax = fig.add_subplot(1, 1, 1)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_xticks(ind)
    ax.set_xticklabels(x_ticklabels)
    ax.bar(ind, y_values, align='center')
 
    ret = StringIO.StringIO()
    canvas.print_figure(ret)
    return base64.b64encode(ret.getvalue())
