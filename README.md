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

A Python tool inspired by Header Hero for tracking down all your awful
C and C++ header dependency problems.

Example
-------

python headerchamp.py -I project/relative/include/dir/1 -I
project/relative/include/dir/2 -I /system/include/dir project_dir

Output
------
<count> <lines> <total_lines> <filename>

Column 3 is the overal count (in lines processed) of that header,
column 2 is the cost of including it once.
