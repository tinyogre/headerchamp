Header Champ
============

version 0.01
------------

Licensing
---------
Copyright (c) 2011 Joe Rumsey

Released under the MIT License, see LICENSE for details

About
-----

A Python (with a web server) tool inspired by Header Hero for tracking
down all your awful C and C++ header dependency problems.

Requirements
------------
Python  
Tornado  
SCons (Or just copy some files manually)  

Installation
------------
    git submodule init
    scons

Example
-------

    python headerchamp.py -I project/relative/include/dir/1 -I project/relative/include/dir/2 -I /system/include/dir -p project_dir

Or run it as a web server:

    python server.py -I project/relative/include/dir/1 -I project/relative/include/dir/2 -I /system/include/dir -p project_dir

	Open http://localhost:8888/ in a browser

