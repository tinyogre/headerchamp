#!/usr/bin/env python

import os, sys
import re
import argparse
inc = re.compile('^\s*#include\s*[<"](.*)[>"]')

headers = {}
def file_size(file):
    f = open(file, 'r')
    count = 0
    for l in f:
        count += 1
    f.close()
    return count

def add_header(chkpath):
    if chkpath in headers:
        headers[chkpath]['count'] += 1
    else:
        headers[chkpath] = {
            'count': 1,
            'size': file_size(chkpath)
            }

def parse(filename, in_dir):
    #print filename
    f = open(filename, 'r')
    for line in f:
        m = inc.match(line)
        if m:            
            for id in [in_dir] + include_dirs:
                found = False
                chkpath = os.path.join(id, m.group(1))
                if os.path.exists(chkpath):
                    #print chkpath
                    found = True
                    add_header(chkpath)
                    break
            if not found and args['warn_missing_files']:
                print m.group(1) + ' was not found while parsing %s in %s' % (filename, in_dir)
    f.close()


def walk(dirname):
    for dir, dirs, files in os.walk(dirname):
        for file in [f for f in files if f.endswith('.cpp')]:
            parse(os.path.join(dir, file), dir)

sys_dirs=['/usr/include', '/usr/local/include']
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse a C/C++ project for header dependencies')
    parser.add_argument('-I', '--include-dir', action='append')
    parser.add_argument('-W', '--warn-missing-files', action='store_true', default=False)
    parser.add_argument('projectdir', metavar='projectdir')
    args = vars(parser.parse_args())
    projdir = args['projectdir']
    include_dirs = sys_dirs + args['include_dir']

    #print args['include_dir']
    #print include_dirs
    #print args

    os.chdir(args['projectdir'])
    walk('.')

    for k,v in headers.items():
        print '%d %d %d %s' %(v['count'], v['size'], v['count'] * v['size'], k)
