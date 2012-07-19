#! /usr/bin/env python
#
#Copyright (c) 2012 Robert Rouhani <robert.rouhani@gmail.com>
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import pkgutil
import vgf
    
def print_help():
    print "Video Game Format Utilities"
    print "Usage: vgfutil.py <game> <format> <command> [options] <file>"
    print ""
    print "The <game> argument must be the name of a properly-formatted package."
    print "The <format> argument must be a file-format module within the <game> package."
    print ""
    print "Additional help for games and formats are available by entering only entering"
    print "the <game> and <game> <format> arguments, respectively."
    print ""
    print "Available Games:"
    package = vgf
    for importer, modname, ispkg in pkgutil.walk_packages(package.__path__,
                                                          onerror=lambda x: None):
        if ispkg:
            print "    " + modname

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        try:
            import_string = "from vgf." + sys.argv[1] + ".cli_main import main"
            exec import_string
        except SyntaxError:
            print "ERROR: Game", sys.argv[1], "cannot be found."
            print_help()
        main_string = "main(sys.argv[2:len(sys.argv)])"
        exec main_string
    else:
        print_help()