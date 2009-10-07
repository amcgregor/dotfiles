"""
Taken from: http://www.codexon.com/posts/clearing-passwords-in-memory-with-python
"""

def zerome(string):
    # find the header size with a dummy string
    temp = "finding offset"
    header = ctypes.string_at(id(temp), sys.getsizeof(temp)).find(temp)
 
    location = id(string) + header
    size     = sys.getsizeof(string) - header
 
    memset =  ctypes.cdll.msvcrt.memset
    # For Linux, use the following. Change the 6 to whatever it is on your computer.
    # memset =  ctypes.CDLL("libc.so.6").memset
 
    print "Clearing 0x%08x size %i bytes" % (location, size)
 
    memset(location, 0, size)