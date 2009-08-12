# encoding: utf-8

import sys, os, shutil, re


class BaseGatherer(object):
    def __init__(self, config={}):
        super(BaseGatherer, self).__init__()
    
    def __call__(self, path):
        for root, folders, files in os.walk(path):
            yield ('d', root)
            
            for folder in folders:
                yield ('d', os.path.join(root, folder))
                
            for phile in files:
                yield ('f', os.path.join(root, phile))


class DictObject(dict):
    def __getattr__(self, attr):
        if attr in self.__dict__: return self.__dict__[attr]
        return self[attr]


class RegexGatherer(BaseGatherer):
    def __init__(self, config={}):
        super(RegexGatherer, self).__init__(config)
        
        self.filters = DictObject(
            path = re.compile(config['path_filter']) if 'path_filter' in config else None,
            folder = re.compile(config['folder_filter']) if 'folder_filter' in config else None,
            file = re.compile(config['file_filter']) if 'file_filter' in config else None
        )
    
    def __call__(self, path):
        for root, folders, files in os.walk(path):
            if ( self.filters.path and self.filters.path.match(root) ) or ( self.filters.folder and self.filters.folder.match(os.path.basename(root)) ):
                for folder in folders: folders.remove(folder)
                continue

            yield ('d', root)

            for folder in folders:
                if self.filters.path and self.filters.folder.path(os.path.join(root, folder)):
                    folders.remove(folder)
                    continue

                if self.filters.folder and self.filters.folder.match(folder):
                    folders.remove(folder)
                    continue

            for phile in files:
                path = os.path.join(root, phile)

                if self.filters.path and self.filters.path.match(path):
                    continue

                if self.filters.file and self.filters.file.match(phile):
                    continue

                yield ('f', path)
        

if __name__ == '__main__':
    gather = BaseGatherer()
    count = 0
    files = []

    print "%15d objects found\r" % count,

    for i in gather(sys.argv[1]):
        count = count + 1
        if count % 1000 == 0:
            print "%15d\r" % count,

    print "%15d objects found" % count