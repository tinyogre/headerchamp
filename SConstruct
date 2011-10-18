env = Environment()

js_src = Split("""
XRegExp
shCore
shBrushCpp
shBrushCSharp
""")

css_src=Split("""
shCore
shThemeEmacs
shThemeDefault
shThemeMidnight
""")

output = []
for j in js_src:
    output = env.Command('static/js/' + j + '.js', 'SyntaxHighlighter/scripts/' + j + '.js',
                         Copy("$TARGET", "$SOURCE"))

for c in css_src:
    output = env.Command('static/css/' + c + '.css', 'SyntaxHighlighter/styles/' + c + '.css',
                         Copy("$TARGET", "$SOURCE"))
