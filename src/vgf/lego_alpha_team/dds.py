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

import os
import struct

class DDSFile:
    def __init__(self, path):
        if not os.path.isfile(path):
            raise ValueError("path is not a file.")
        self.path = path
        self.len_data = os.stat(path).st_size
        
    def save_as_wav(self, out_path):
        with open(self.path, "rb") as in_f:
            with open(out_path, "w+b") as out_f:
                self.__write_wav_header(out_f)
                out_f.write(in_f.read(self.len_data))
                
    def __write_wav_header(self, f):
        f.write(struct.pack('<4si4s', "RIFF", self.len_data + 36, "WAVE"))
        f.write(struct.pack('<4si2h2i2h', "fmt\x20", 16, 1, 1, 44100, 88200, 2, 16))
        f.write(struct.pack('<4si', "data", self.len_data))