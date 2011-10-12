
import tornado.ioloop
import tornado.web
import tornado.template
import headerchamp

from operator import itemgetter, attrgetter

HEADER = '<html><body>'
FOOTER = '</body></html>'

sources = None

loader = tornado.template.Loader('templates')

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        global sources
        if not sources:
            sources = []
            for k,v in headerchamp.sources.items():
                sources.append(v)
            
            sources.sort(key=attrgetter('total_cost'), reverse=True)
        
        self.write(loader.load('index.html').generate(sources=sources))

class FileHandler(tornado.web.RequestHandler):
    def get(self, filename):
        global sources
        header = headerchamp.sources[filename]
        self.write(loader.load('file.html').generate(header=header, all_sources = headerchamp.sources))

application = tornado.web.Application([
        (r'/', MainHandler),
        (r'/file/(.*)', FileHandler),
])

if __name__=="__main__":
    application.listen(8888)
    headerchamp.run()
    tornado.ioloop.IOLoop.instance().start()

