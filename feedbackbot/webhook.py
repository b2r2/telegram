import cherrypy


class WebhookServer(object):
    def __init__(self, bot, types):
        self.bot = bot
        self.types = types

    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                'content-type' in cherrypy.request.headers and \
                cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode('utf-8')
            update = self.types.Update.de_json(json_string)
            self.bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)
