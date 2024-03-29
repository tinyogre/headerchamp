#!/usr/bin/env python

import os, sys
import re
import argparse
from graph import graph

inc = re.compile('^\s*#include\s*[<"](.*)[>"]')

class Source:
    def __init__(self, name, count, size, is_src = False):
        self.name = name
        self.count = count
        self.size = size
        self.included_by = set()
        self.includes = set()
        self.is_src = is_src
        self.path=os.path.join(os.getcwd(), name)
        self.include_line_nums = []
        self.child_size = 0

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
    return sources[header].size + sources[header].child_size

def parse(filename, in_dir, recursed):
    filename = os.path.normpath(filename)
    if not filename in sources:
        sources[filename] = Source(filename, 0, file_size(filename), True)

    src = sources[filename]

    #print filename
    f = open(filename, 'r')
    line_num = 0
    src.child_size = 0
    for line in f:
        line_num += 1
        m = inc.match(line)
        if m:            
            src.include_line_nums.append(line_num)
            for id in [in_dir] + include_dirs:
                found = False
                chkpath = os.path.normpath(os.path.join(id, m.group(1)))
                if os.path.exists(chkpath):
                    #print chkpath
                    found = True
                    src.child_size += add_header(chkpath, os.path.normpath(filename))
                    src.includes.add(chkpath)
                    break
            if not found and args['warn_missing_files']:
                print m.group(1) + ' was not found while parsing %s in %s' % (filename, in_dir)
    sources[filename] = src
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
    parser.add_argument('-g', '--graph')
    parser.add_argument('-t', '--table', action='store_true', default = False)

    parser.add_argument('-p', '--projectdir', metavar='projectdir')
    parser.add_argument('-s', '--scandir', action='append')

    args = vars(parser.parse_args())
    projdir = args['projectdir']
    include_dirs = sys_dirs + args['include_dir']
    scan_dirs = args['scandir']
    if not scan_dirs:
        scan_dirs = ['.']

    #print args['include_dir']
    #print include_dirs
    #print args
    pwd = os.getcwd()
    os.chdir(args['projectdir'])
    for d in scan_dirs:
        walk(d)
    os.chdir(pwd)

    for h in sources.values():
        h.finalize()

    if 'graph' in args:
        if args['graph'] == '-':
            f = None
        else:
            f = open(args['graph'], 'w')
        graph(sources, f)
        if f:
            f.close()

    if 'table' in args and args['table']:
        for k,v in sources.items():
            print '%d %d %d %s' %(v.count, v.size, v.count * v.size, k)

if __name__ == "__main__":
    run()


