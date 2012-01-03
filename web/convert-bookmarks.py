#!/usr/bin/env python -u
# encoding: utf-8

"""Convert JSON-style bookmarks into a standard HTML page."""

from __future__ import unicode_literals, print_function

import sys
from json import loads
from marrow.tags.html5 import *
from pprint import pprint


headers = [None, h1, h2, h3, h4, h5, h6]



def extract(node, level=1):
    """This is a recursive algorithm, meaning it calls itself.
    
    This is non-optimum for heavily nested data sets.
    """
    
    print("%sExporting bookmarks from:" % ("    " * (level-1), ), node['name'])
    parts = [ dt [ headers[level] [ node['name'] ] ], dl [ p() ] ]
    list_ = parts[1].children[0].children
    
    if level > 1:
        parts.insert(0, hr)
    
    if "children" in node:
        links = [child for child in node['children'] if child['type'] == "url"]
        
        if links:
            # Loop through all links and add them to an ordered list.
            for i, child in enumerate(links):
                print("\r\033[K%sExporting link %d of %d... %s" % ("    " * (level-1), i+1, len(links), child['name']), end="")
                
                list_.append(dt [ a ( href = child['url'] ) [ child['name'] ] ])
            
            print("\r\033[K%sExporting link %d of %d... done." % ("    " * (level-1), len(links), len(links)))
        
        else:
            print("WTF, no links?")
        
        del links
        
        # Loop through all folders and add them as sub-headings.
        for child in [child for child in node['children'] if child['type'] == "folder"]:
            parts.extend(extract(child, level+1))
    
    else:
        print("That's strange; no child nodes.")
    
    return parts


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as fh:
        data = loads(fh.read().decode('utf8'))
    
    mock = {'name': "Your Bookmarks, Madam", 'children': list(data['roots'].itervalues())}
    
    result = div ( strip = True ) [
            meta ( **{b'http-equiv': "Content-Type", b'content': "text/html; charset=UTF-8"} ),
            title [ "Bookmarks" ],
            dl [ p [ extract(mock) ] ]
        ]
    
    with open(sys.argv[1] + '.html', 'w') as fh:
        fh.write("<!DOCTYPE NETSCAPE-Bookmark-file-1>\n")
        for chunk in result.render('utf8'):
            fh.write(chunk)
