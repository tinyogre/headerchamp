import sys

def graph(sources, file = None):
    if file is None:
        file = sys.stdout
    file.write('digraph project {\n')

    for name, s in sources.items():
        for inc in s.includes:
            if s.is_src:
                file.write('"%s" [color="#aaffff"];\n' % s.name)
            file.write('"%s" -> "%s";\n' % (s.name, inc))
    file.write('}\n')
