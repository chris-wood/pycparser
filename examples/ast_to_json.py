#-----------------------------------------------------------------
# pycparser: ast_to_json.py
#
# Output the JSON representation of the parsed AST
#
# Copyright (C) 2008-2011, Eli Bendersky
# Copyright (C) 2015, Christopher A. Wood
# License: BSD
#-----------------------------------------------------------------
from __future__ import print_function
import sys
import re

# This is not required if you've installed pycparser into
# your site-packages/ with setup.py
#
sys.path.extend(['.', '..'])

from pycparser import c_parser, c_ast, parse_file

def comment_remover(text):
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return " " # note: a space and not an empty string
        else:
            return s
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, replacer, text)

# A visitor with some state information (the funcname it's
# looking for)
#
class FuncCallVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.rawr = ""

    def visit_FuncCall(self, node):
        print('called at %s' % (node.name.coord))

# class RenderVisitor(c_ast.NodeVisitor):
#     def __init__(self):
#         self.json = ""

#     def visit_FuncCall(self, node):
#         self.json = "["
#         for c in node.children:

class ConstantVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.values = []

    def visit_Constant(self, node):
        self.values.append(node.value)

def render_json(filename):

    # Create the parser and ask to parse the text. parse() will throw
    # a ParseError if there's an error in the code
    #
    parser = c_parser.CParser()

    fileIn = open(filename, "r")
    lines = []
    for line in fileIn.readlines():
        if not line.startswith("#"):
            lines.append(line)
    text = comment_remover(''.join(lines))

    # print(text)
    ast = parser.parse(text)
    # ast.show()

    renderer = RenderVisitor()
    renderer.visit(ast)
    print(renderer.json)
    # jsonString = renderer.getJSONString()

if __name__ == "__main__":
    filename = ""
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'c_files/hash.c'

    render_json(filename)
