
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

def get_src(source):
    f = open(source.path, 'r')
    text = f.read()
    f.close()
    highlights='['
    first = True
    for l in source.include_line_nums:
        if not first:
            highlights += ','
        else:
            first = False
        highlights += str(l)
    highlights += ']'
    return text, highlights

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
        source = headerchamp.sources[filename]
        text, highlights = get_src(source)
        self.write(loader.load('file.html').generate(source=source, 
                                                     text = text, 
                                                     highlights = highlights, 
                                                     all_sources = headerchamp.sources))

class SourceHandler(tornado.web.RequestHandler):
    def get(self, filename):
        global sources
        source = headerchamp.sources[filename]
        text, highlights = get_src(source)

        self.write(loader.load('source.html').generate(source=source, highlights=highlights, text=text))

settings = {
    'static_path': os.path.join(os.getcwd(), 'static'),
}
    
application = tornado.web.Application([
        (r'/', MainHandler),
        (r'/file/(.*)', FileHandler),
        (r'/source/(.*)', SourceHandler),
], **settings)

if __name__=="__main__":
    application.listen(8888)
    print "Processing..."
    headerchamp.run()
    print "Ready!"
    tornado.ioloop.IOLoop.instance().start()

