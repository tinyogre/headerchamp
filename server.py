
import tornado.ioloop
import tornado.web
import headerchamp

from operator import itemgetter

HEADER = '<html><body>'
FOOTER = '</body></html>'

headers = None

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        global headers
        self.write(HEADER)

        self.write('<table>\n')
        if not headers:
            headers = []
            for k,v in headerchamp.headers.items():
                headers.append((k, v['count'], v['size'], v['count'] * v['size']))
            
            headers.sort(key=itemgetter(3), reverse=True)
        
        for h in headers:
            self.write('<tr><td>%d</td><td>%d</td><td>%d</td><td><a href="/file/%s">%s</a></td></tr>\n' % (h[1], h[2], h[3], h[0], h[0]))
        self.write('</table>')

        self.write(FOOTER)

class FileHandler(tornado.web.RequestHandler):
    def get(self, filename):
        global headers
        self.write(HEADER)
        self.write('<H1>%s</H1>\n' % (filename))
        self.write('<table>')
        info = headerchamp.headers[filename]
        self.write('<tr><td>Lines</td><td>%d</td></tr>' % (info['size']))
        self.write('<tr><td>Count</td><td>%d</td></tr>' % (info['count']))
        self.write('<tr><td>Total Count</td><td>%d</td></tr>' % (info['count'] * info['size']))
        self.write('</table>\n')
        self.write('<H2>Included by</H2>\n')
        for ib in headerchamp.headers[filename]['included_by']:
            if ib in headerchamp.headers:
                self.write('<p><a href="/file/%s">%s</a></p>\n' % (ib, ib))
            else:
                self.write('<p>%s</p>\n' % (ib))

        self.write(FOOTER)

application = tornado.web.Application([
        (r'/', MainHandler),
        (r'/file/(.*)', FileHandler),
])

if __name__=="__main__":
    application.listen(8888)
    headerchamp.run()
    tornado.ioloop.IOLoop.instance().start()

