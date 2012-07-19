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

from pac import PACFile
from dds import DDSFile
from misc import pathhelper
import os

def main(args):
    if len(args) > 0:
        if args[0] == "pac":
            handle_pac_command(args[1:len(args)])
        elif args[0] == "dds":
            handle_dds_command(args[1:len(args)])
        else:
            print_help()
    else:
        print_help()
            
    
def print_help():
    print "LEGO Alpha Team Utilities"
    print "Usage: vgfutil.py lego_alpha_team <command> [options] <file>"
    print ""
    print "Available Formats:"
    print "    pac"
    print "    dds"
   
def print_help_pac():
    print "LEGO Alpha Team .pac Extractor"
    print "Usage: vgfutil.py lego_alpha_team pac <command> [options] <file>"
    print ""
    print "Example: vgfutil.py lego_alpha_team pac extract all ./audio Audio.pac"
    print ""
    print "All commands have the available option 'all' to execute the command for all"
    print "entries in the file."
    print ""
    print "Available Commands (with options):"
    print "    extract [all|<entry name>] [output path]"
    print "    list    [all|<entry name>]"
   
def print_help_dds():
    print "LEGO Alpha Team .dds Converter"
    print "Usage: vgfutil.py lego_alpha_team dds <command> [options] <file>"
    print ""
    print "Example: vgfutil.py lego_alpha_team dds convert out.wav in.dds"
    print "Example: vgfutil.py lego_alpha_team dds convert ./out ./audio"
    print ""
    print "Available Commands (with options):"
    print "    convert [<output dir>|<output file>] [<dir>|<file>]"
   
def handle_pac_command(args):
    if len(args) >= 3:
        f = PACFile(args[len(args) - 1])
        if args[0] == "list":
            if args[1] == "all":
                f.print_all_entries()
            else:
                f.print_entry(args[1])
        elif args[0] == "extract":
            if args[1] == "all":
                if len(args) == 4:
                    f.extract_all(args[2])
                else:
                    f.extract_all(".")
            elif len(args) == 4:
                f.extract(args[1], args[2])
            else:
                f.extract(args[1], ".")
    else:
        print_help_pac()
    
def handle_dds_command(args):
    if len(args) == 3:
        if args[0] == "convert":
            if os.path.isdir(args[2]):
                if not os.path.exists(args[1]):
                    os.makedirs(args[1])
                for in_filepath in os.listdir(args[2]):
                    if (in_filepath.endswith(".DDS")):
                        out_filepath = pathhelper.new_ext_and_path(in_filepath, ".wav", args[1])
                        DDSFile(os.path.join(args[2], in_filepath)).save_as_wav(out_filepath)
            elif os.path.isfile(args[2]):
                out_filepath = args[1]
                if not out_filepath.endswith(".wav"):
                    out_filepath.join(".wav")
                DDSFile(args[2]).save_as_wav(out_filepath)
            else:
                print_help_dds()
        else:
            print_help_dds()