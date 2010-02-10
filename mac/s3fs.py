#!/usr/bin/env python

import json, cStringIO

from collections import defaultdict
from errno import ENOENT
from stat import S_IFDIR, S_IFLNK, S_IFREG
from sys import argv, exit
from time import time

from boto.s3.connection import S3Connection

from fuse import FUSE, Operations, LoggingMixIn




# TODO: Pull security credentials from a configuration file combined from /etc/s3fs.conf, ~/.s3fs.conf, and the command line.
# [default] section, and [bucketname] individual sections.

BUCKET = "s3fspy"
KEY = "124P4766WQW628N9TMG2"
SECRET = "aNQNbHWMjsdl8HklbBWm8lNJx6oblkVwa/NhIFKw"

MODE_FILE = 0644
MODE_DIR = 0755

CACHE = defaultdict(dict)


def def_stat():
    now = time()
    
    return dict(
            st_mode=(S_IFREG | 0755),
            st_ctime=now,
            st_mtime=now,
            st_atime=now,
            st_nlink=1
        )
    


class S3FS(LoggingMixIn, Operations):
    """Amazon S3 FUSE interface using """
    
    def __init__(self):
        self.cache = defaultdict(def_stat)
        self.fd = 0
        
        self.connection = S3Connection(KEY, SECRET, host='s3.amazonaws.com', path='/', is_secure=True, port=None, proxy=None, proxy_port=None, proxy_user=None, proxy_pass=None)
        self.bucket = self.connection.get_bucket(BUCKET) # create_bucket(BUCKET, location=''||Location.EU)
        
        now = time()
        
        self.cache['/'] = dict(
                st_mode=(S_IFDIR | 0755),
                st_ctime=now,
                st_mtime=now,
                st_atime=now,
                st_nlink=2
            )
        
    def readdir(self, path, fh):
        prefix = path[1:] + '/' if path != '/' else ''
        iterator = self.bucket.list(prefix=prefix, delimiter='/')
        elements = []
        
        print repr(path)
        
        for i in iterator:
            if i.name == prefix: continue
            
            elements.append((i.name.encode('utf8') if isinstance(i.name, unicode) else i.name).strip('/')[len(prefix):])
            
            now = time()
            fpath = '/' + i.name.strip('/')
            
            print repr(prefix), repr(i.name), repr(fpath)
            
            if i.name.endswith('/'):
                self.cache[fpath] = dict(
                        st_mode=(S_IFDIR | 0755),
                        st_ctime=now,
                        st_mtime=now,
                        st_atime=now,
                        st_nlink=2
                    )
            
            else:
                self.cache[fpath] = dict(
                        st_mode=(S_IFREG | 0644),
                        st_size=i.size,
                        st_ctime=now,
                        st_mtime=now, # last_modified
                        st_atime=now,
                        st_nlink=1
                    )

        return ['.', '..'] + elements

    def chmod(self, path, mode):
        """Change the mode on the file.
        
        This controls the ACL on S3.
        
        The only flags currently used are the world flags:
        
        0: Private
        4: Read-Only
        6: Read-Write
        
        Other bits are currently ignored, but cached locally for your convienence.
        
        Alternatively, preserve all bits as metadata.
        """
        
        self.cache[path]['st_mode'] &= 0770000
        self.cache[path]['st_mode'] |= mode
        
        mode = mode & 0777771
        print "**** new mode: %o" % (mode, )
        
        modes = {0: "private", 4: "public-read", 6: "public-read-write"}
        
        self.bucket.set_acl(modes[mode], path[1:])
        
        return 0

    def chown(self, path, uid, gid):
        """Change the file ownership.
        
        This can be saved as metadata in S3, and will likely not translate well across machines.
        
        Currently only cached locally for your convienence.
        """
        self.cache[path]['st_uid'] = uid
        self.cache[path]['st_gid'] = gid
    
    def create(self, path, mode):
        """Create a new file with the given mode."""
        
        self.cache[path] = dict(
                st_mode=(S_IFREG | mode),
                st_nlink=1,
                st_size=0,
                st_ctime=time(),
                st_mtime=time(),
                st_atime=time()
            )
        
        k = self.bucket.new_key(path[1:])
        k.set_contents_from_string('')
        
        # TODO: Handle mode.
        
        self.fd += 1
        
        return self.fd
    
    def getattr(self, path, fh=None):
        """Read the attributes of the given path."""
        
        print "getattr: %r" % (path, )
        if path not in self.cache:
            print repr(self.cache)
            raise OSError(ENOENT, '')
        
        st = self.cache[path]
        
        return st
    
    def getxattr(self, path, name, position=0):
        attrs = self.cache[path].get('attrs', {})
        
        try:
            return attrs[name]
        
        except KeyError:
            return ''       # Should return ENOATTR
    
    def listxattr(self, path):
        attrs = self.cache[path].get('attrs', {})
        
        return attrs.keys()
    
    def mkdir(self, path, mode):
        """Empty directories are a local construct only; if left empty when the connection is closed, the folder is gone."""
        
        self.cache[path] = dict(
                st_mode=(S_IFDIR | mode),
                st_nlink=2,
                st_size=0,
                st_ctime=time(),
                st_mtime=time(),
                st_atime=time()
            )
        
        self.cache['/']['st_nlink'] += 1
    
    def open(self, path, flags):
        self.fd += 1
        return self.fd
    
    def read(self, path, size, offset, fh):
        return self.bucket.get_key(path[1:]).get_contents_as_string(headers=dict(Range="%d-%d" % (offset, offset + size)))
    
    def readlink(self, path):
        raise Exception()
        # return self.data[path]
    
    def removexattr(self, path, name):
        attrs = self.cache[path].get('attrs', {})
        
        try:
            del attrs[name]
        
        except KeyError:
            pass        # Should return ENOATTR
    
    def rename(self, old, new):
        k = self.bucket.get_key(old)
        k.copy(BUCKET, new)
        k.delete()
        self.cache[new] = self.cache.pop(old)
    
    def rmdir(self, path):
        for i in self.bucket.list(path[1:]):
            i.delete()
        
        self.cache.pop(path)
        self.cache['/']['st_nlink'] -= 1
    
    def setxattr(self, path, name, value, options, position=0):
        # Ignore options
        attrs = self.cache[path].setdefault('attrs', {})
        attrs[name] = value
    
    def statfs(self, path):
        return dict(f_bsize=512, f_blocks=4096, f_bavail=2048)
    
    def symlink(self, target, source):
        return
        
        #self.cache[target] = dict(st_mode=(S_IFLNK | 0777), st_nlink=1, st_size=len(source))
        #self.data[target] = source
    
    def truncate(self, path, length, fh=None):
        k = self.bucket.get_key(path[1:])
        contents = k.get_contents_as_string(headers=dict(Range="0-%d" % (length, )))
        k.set_contents_from_string(contents)
        self.cache[path]['st_size'] = length
    
    def unlink(self, path):
        self.bucket.delete(path[1:])
        self.cache.pop(path)
    
    def utimens(self, path, times=None):
        now = time()
        atime, mtime = times if times else (now, now)
        self.cache[path]['st_atime'] = atime
        self.cache[path]['st_mtime'] = mtime
    
    def write(self, path, data, offset, fh):
        # TODO: Handle reads/writes by downloading the file into a temporary file handle, and passing calls through.
        # Only commit to S3 when the file handle is closed.
        # As it is, it is unwise to handle large files!
        
        k = self.bucket.get_key(path[1:])
        contents = k.get_contents_as_string()[:offset] + data
        
        k.set_contents_from_string(contents)
        
        self.cache[path]['st_size'] = len(contents)
        return len(data)


if __name__ == "__main__":
    if len(argv) != 2:
        print 'usage: %s <mountpoint>' % argv[0]
        exit(1)
    fuse = FUSE(S3FS(), argv[1], foreground=True)
