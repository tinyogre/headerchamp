
import tornado.ioloop
import tornado.web
import tornado.template
import headerchamp
import os

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

settings = {
    'static_path': os.path.join(os.getcwd(), 'static'),
}
    
application = tornado.web.Application([
        (r'/', MainHandler),
        (r'/file/(.*)', FileHandler),
], **settings)

if __name__=="__main__":
    application.listen(8888)
    print "Processing..."
    headerchamp.run()
    print "Ready!"
    tornado.ioloop.IOLoop.instance().start()

