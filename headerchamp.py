#!/usr/bin/env python

import os, sys
import re
import argparse
inc = re.compile('^\s*#include\s*[<"](.*)[>"]')

class Source:
    def __init__(self, name, count, size):
        self.name = name
        self.count = count
        self.size = size
        self.included_by = set()
        self.includes = set()

    def finalize(self):
        self.total_cost = self.count * self.size

    def add_included_by(self, included_by):
        self.included_by.add(included_by)

sources = {}
def file_size(file):
    f = open(file, 'r')
    count = 0
    for l in f:
        count += 1
    f.close()
    return count

def add_recursive_count(sub, visited):
    if not sub in sources:
        return

    src = sources[sub]
    src.count += 1
    for h in src.includes:
        if not h in visited:
            visited.add(h)
            add_recursive_count(h, visited)

def add_header(header, included_by):
    if not header in sources:
        #print 'added: ' + header
        h = Source(header, 0, file_size(header))
        sources[header] = h
        parse(header, os.path.split(header)[0], True)
    else:
        h = sources[header]
        add_recursive_count(header, set())

    h.count += 1
    if included_by:
        h.add_included_by(included_by)

def parse(filename, in_dir, recursed):
    filename = os.path.normpath(filename)
    if not filename in sources:
        sources[filename] = Source(filename, 0, 0)

    src = sources[filename]

    #print filename
    f = open(filename, 'r')
    for line in f:
        m = inc.match(line)
        if m:            
            for id in [in_dir] + include_dirs:
                found = False
                chkpath = os.path.normpath(os.path.join(id, m.group(1)))
                if os.path.exists(chkpath):
                    #print chkpath
                    found = True
                    add_header(chkpath, os.path.normpath(filename))
                    src.includes.add(chkpath)
                    break
            if not found and args['warn_missing_files']:
                print m.group(1) + ' was not found while parsing %s in %s' % (filename, in_dir)
    f.close()


def walk(dirname):
    for dir, dirs, files in os.walk(dirname):
        for file in [f for f in files if f.endswith('.cpp')]:
            #print os.path.join(dir, file)
            parse(os.path.join(dir, file), dir, False)

sys_dirs=['/usr/include', '/usr/local/include']
include_dirs = []
def run():
    global args, include_dirs
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

    for h in sources.values():
        h.finalize()

if __name__ == "__main__":
    run()

    for k,v in sources.items():
        print '%d %d %d %s' %(v.count, v.size, v.count * v.size, k)

