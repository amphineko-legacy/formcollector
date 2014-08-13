from config import getNetwork, getPlugins
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler, url

class PFLServer:
    class CommitHandler(RequestHandler):
        def initialize(self, plugins):
            self.plugins = plugins

        def get(self):
            self.render('./static/rejected.html', reason = 'Bad request.')

        def post(self):
            body = self.request.body;
            if body:
                if self.plugins['validate']:
                    (valid, reason) = self.plugins['validate'].validate(body);
                else:
                    valid = True
                if valid:
                    self.plugins['logger'].log(body)
                    self.render('./static/accepted.html')
                else:
                    self.render('./static/rejected.html', reason = reason)
            else:
                self.render('./static/rejected.html', reason = 'Bad request.')

    def __init__(self):
        network = getNetwork()
        self.plugins = getPlugins()
        self.app = self.createApplication(network, self.plugins)
        self.app.listen(network['http_port'])
        IOLoop.current().start()

    def createApplication(self, nw, plugins):
        return Application([
            url(nw['path_commit'], self.CommitHandler, dict(plugins = plugins))
        ])

if __name__ == '__main__':
    PFLServer()
