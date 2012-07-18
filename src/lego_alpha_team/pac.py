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

from miscutils.filetimes import filetime_to_dt
import struct
import os

#see doc/lego-alpha-team/pac.txt for more information on the file format

class PACEntry:
    def __init__(self, name, size, offset, timestamp):
        self.name = name
        self.size = size
        self.offset = offset
        self.timestamp = filetime_to_dt(timestamp)
        
    def __str__(self):
        return self.name + ": Size=" + str(self.size) + " Offset=" + str(self.offset) + " Last Modified=" + str(self.timestamp)

class PACFile:

    def __init__(self, path):
        self.path = path
        self.files = []
        with open(path, "rb") as f:
            header = struct.unpack("<4s4I", f.read(20))
            if header[0] != "PACK":
                raise ValueError("File is not a valid .pac file")
            if header[1] != os.stat(path).st_size:
                raise ValueError("File is not a valid .pac file")
            self.num_subdirs = header[2]
            self.ofs_data = header[3]
            self.num_files = header[4]
            self.__parse_entries(f)
            
    def extract_all(self):
        f = open(self.path, "rb")
        for entry in self.files:
            self.__extract_entry(f, entry)
        f.close()
    
    def extract(self, entry):
        f = open(self.path, "rb")
        if isinstance(entry, PACEntry):
            self.__extract_entry(f, entry)
        else:
            try:
                entry_obj = next(e for e in self.files if e.name == entry)
                self.__extract_entry(f, entry_obj)
            except StopIteration:
                raise ValueError("Entry '" + entry + "' cannot be found.")
        f.close()
        
    def print_entry(self, entry):
        try:
            entry = next(e for e in self.files if e.name == entry)
            print entry
        except StopIteration:
            raise ValueError("Entry '" + entry + "' cannot be found.")
            
    def print_all_entries(self):
        for entry in self.files:
            print entry
    
    def __parse_entries(self, f):
        with open(self.path, "rb") as f:
            f.seek(20)
            for i in range(0, self.num_files):
                entry_name = self.__parse_name(f)
                entry_info = struct.unpack("<3I", f.read(12))
                entry_timestamp = struct.unpack("q", f.read(8))
                self.files.append(PACEntry(entry_name, entry_info[2],
                                            entry_info[1], entry_timestamp[0]))
    
    def __parse_name(self, f):
        str_list = []
        cur_char = f.read(1)
        while cur_char != "\x00":
            str_list.append(cur_char)
            cur_char = f.read(1)
        return ''.join(str_list)
        
    def __extract_entry(self, f, entry):
        f.seek(entry.offset)
        with open(entry.name, "w+b") as outfile:
            outfile.write(f.read(entry.size))