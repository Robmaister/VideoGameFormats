import struct
import os

#see doc/lego-alpha-team/pac.txt

class PACEntry:
    def __init__(self, name, size, offset, timestamp):
        self.name = name
        self.size = size
        self.offset = offset
        self.timestamp = timestamp

class PACFile:

    def __init__(self, path):
        self.path = path
        self.files = []
        with open(path, "rb") as file:
            header = struct.unpack("<4sIIII", file.read(20))
            if header[0] != "PACK":
                raise TypeError("File is not a .pac file")
            if header[1] != os.stat(path).st_size:
                raise TypeError("File is not a .pac file")
            self.num_subdirs = header[2]
            self.ofs_data = header[3]
            self.num_files = header[4]
            self.__parse_header(file)
            
    def extract_all(self):
        file = open(self.path, "rb")
        for entry in self.files:
            self.__save_entry(file, entry)
                    
    
    def extract(self, file_entry):
        file = open(self.path, "rb")
        if not isinstance(file_entry, PACEntry):
            self.__save_entry(file, file_entry)
        else:
            try:
                entry = next(e for e in self.files if e.name == file_entry)
                self.__save_entry(file, entry)
            except StopIteration:
                print "File '" + file_entry + "' can't be found."
        file.close()
    
    def list_entries(self):
        for entry in self.files:
            print "File:", entry.name
            print "\tSize:", entry.size
            print "\tOffset:", entry.offset
    
    def __parse_header(self, file):
        with open(self.path, "rb") as file:
            file.seek(20)
            for i in range(0, self.num_files):
                entry_data = struct.unpack("<IIIq", file.read(20))
                self.files.append(PACEntry(self.__parse_name(file),
                    entry_data[2], entry_data[1], entry_data[3]))
    
    def __parse_name(self, file):
        str_list = []
        chr = file.read(1)
        while chr != "\x00":
            str_list.append(chr)
            chr = file.read(1)
        return ''.join(str_list)
        
    def __save_entry(self, file, entry):
        file.seek(entry.offset)
        with open(entry.name, "w+b") as outfile:
            outfile.write(file.read(entry.size))
    
if __name__ == "__main__":
    import sys
    testFile = PACFile(sys.argv[1])
    testFile.extract_all()