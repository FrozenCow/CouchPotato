from app.lib.qualities import Qualities
from library.minify import Minify
import cherrypy
import routes

def base():
    host = 'http://' + cherrypy.request.headers.get('host')
    base = cherrypy.config.get('config').get('global', 'urlbase')
    base = host + '/' + base if base else host

    return base

def url(*args, **kwargs):
    return cherrypy.url(routes.url_for(*args, **kwargs), base = base())

def redirect(url):
    url = url if url else base()
    raise cherrypy.HTTPRedirect(url)

class BaseController:

    globals = {
        'url': url,
        'Qualities': Qualities(),
        'Minify': Minify()
    }

    def __init__(self):
        self.cron = cherrypy.config.get('cron')
        self.searchers = cherrypy.config.get('searchers')
        self.flash = self.globals['flash'] = cherrypy.config.get('flash')
        self.globals['debug'] = cherrypy.config.get('debug')
        self.globals['updater'] = cherrypy.config.get('updater')
        self.globals['searchers'] = self.searchers
        self.globals['cherrypy'] = cherrypy
        self.globals['config'] = cherrypy.config.get('config')

    def updateGlobals(self):
        base = cherrypy.config.get('config').get('global', 'urlbase')
        host = 'http://' + cherrypy.request.headers.get('host') + '/'

        self.globals['baseUrl'] = host + base + '/' if base else host
        self.globals['yarr'] = self.cron.get('yarr')

    def render(self, list):

        self.updateGlobals()

        list.update(self.globals)

        return list
