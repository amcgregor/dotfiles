#!/usr/bin/env python
# encoding: utf-8

"""

An example version numbering schema system for Distribute.

This allows you to explicitly define (because explicit is better than
implicit) all of the strange versioning schemes your packages may use
throughout its life cycle in a flexible way that can change from
version to version.

The idea is to store the regular expression (or some other description
of the versioning format) within the PKG_INFO metadata file.  With this
it would be possible to accurately version a package despite versioning
method changes.

"""

import re


# Basic versioning; major.minor.bugfix.patch-type-release
version_basic = re.compile(r'(?P<major>\d+)\.(?P<minor>\d+)(?:\.(?P<bugfix>\d+))?(?:\.(?P<patch>\d+))?(?:-?(?P<type>dev|a|alpha|b|beta|pre|rc)(?:-?(?P<release>\d+))?)?')


class Relevance(object):
    """A fake enum to provide reasonable relevance scores for various release types."""
    
    dev = 0
    development = 0
    a = 1
    alpha = 1
    pre = 2
    prerelease = 2
    b = 3
    beta = 3
    rc = 4
    candidate = 4
    final = 5

relevance = Relevance()


class Package(object):
    """A light-weight data container for example use."""
    
    def __init__(self, version, schema=version_basic):
        self.version = version
        self.schema = schema


# Example package with real versioning information.
turbomail = [
        Package('1.0'),
        Package('1.0'),
        Package('1.0.4.2'),
        Package('1.1'),
        Package('1.1.1'),
        Package('1.1.2'),
        Package('2.0'),
        Package('2.0.1'),
        Package('2.0.2'),
        Package('2.0.3'),
        Package('2.0.4'),
        Package('2.1'),
        Package('3.0'),
        Package('3.0.1'),
        Package('3.0.2'),
        Package('3.0.3'),
        Package('3.0.4-dev20091207'),
    ]

examples = [
        # The following two are bad:
        # 1.13++
        # 5.5.kw
        Package('1.5.1', version_basic),
        Package('1.5.2b2', version_basic),
        Package('161', re.compile(r'(?P<release>\d+)')),
        Package('3.10a', version_basic),
        Package('8.02', version_basic),
        Package('1996.07.12', version_basic),
        Package('3.2.pl0', re.compile(r'(?P<major>\d+)\.(?P<minor>\d+)(?:p(?P<bugfix>\d+))?')),
        Package('3.1.1.6', version_basic),
        Package('2g6', re.compile(r'(?P<major>\d+)g(?P<minor>\d+)?(?:p(?P<bugfix>\d+))?')),
        Package('11g', re.compile(r'(?P<major>\d+)g(?P<minor>\d+)?(?:p(?P<bugfix>\d+))?')),
        Package('0.960923', version_basic),
        Package('2.2beta29', version_basic),
        Package('2.0b1pl0', re.compile(r'(?P<major>\d+)\.(?P<minor>\d+)(?:b(?P<bugfix>\d+))?(?:p(?P<patch>\d+))?')),
        Package('0.4', version_basic),
        Package('0.4.0', version_basic),
        Package('0.4.1', version_basic),
        Package('0.5a1', version_basic),
        Package('0.5b3', version_basic),
        Package('0.5', version_basic),
        Package('0.9.6', version_basic),
        Package('1.0', version_basic),
        Package('1.0.4a3', version_basic),
        Package('1.0.4b1', version_basic),
        Package('1.0.4', version_basic)
    ]



def minimal_tuples(packages):
    """Analyze the passed tuples and produce a minimal representation."""
    pass # tbd


def maximal_tuples(packages):
    """Flat out like a lizard drinking."""
    
    parts = (('major', None, int), ('minor', None, int), ('bugfix', None, int), ('patch', None, int), ('type', relevance.final, lambda v: getattr(relevance, v)), ('release', None, int))
    
    pkgs = []
    
    for pkg in packages:
        match = pkg.schema.match(pkg.version)
        
        if not match:
            print pkg.version, "is unmatched"
            continue
        
        components = []
        for i in parts:
            try:
                components.append(i[2](match.group(i[0])) if match.group(i[0]) else i[1])
            except IndexError:
                components.append(i[1])
        
        pkgs.append(tuple(components))
    
    return pkgs


if __name__ == '__main__':
    def consume_two(iterable):
        value = []
        
        for i in iterable:
            value.append(i)
            
            if len(value) == 2:
                yield tuple(value)
                value = []
    
    print "TurboMail Examples:"
    for i, j in consume_two(maximal_tuples(turbomail)):
        print "%r > %r = %r" % (i, j, i > j)
    
    print "\nDistutils Examples:"
    for i, j in consume_two(maximal_tuples(examples)):
        print "%r > %r = %r" % (i, j, i > j)
