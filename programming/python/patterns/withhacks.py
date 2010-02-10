# encoding: utf-8

"""
With statement hacks.

Many of these are blatantly stolen from other locations.

See http://github.com/rfk/withhacks for more.

Craziness:
    http://billmill.org/multi_line_lambdas.html
    http://code.google.com/p/ouspg/wiki/AnonymousBlocksInPython

"""

import time
from contextlib import contextmanager

def timethis(what):
    """Simultaneous context manager and decorator.
    
    Dave Beazley
    http://www.dabeaz.com/blog/2010/02/function-that-works-as-context-manager.html
    """
    
    @contextmanager
    def benchmark():
        start = time.time()
        yield
        end = time.time()
        print("%s : %0.3f seconds" % (what, end-start))
    
    if hasattr(what,"__call__"):
        def timed(*args,**kwargs):
            with benchmark():
                return what(*args,**kwargs)
        
        return timed
    
    else:
        return benchmark()


