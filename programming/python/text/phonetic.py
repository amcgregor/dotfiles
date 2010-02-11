# encoding: utf-8

"""Translate strings of characters into a phonetic representation.

Simply prints out unknown characters as-is.

Designed so that on a Mac you can type:

    echo 'AJFVPKQ12-1293' | python phonetic.py | say

And your computer will actually read out the results, with reasonable pauses.
"""


import sys


alphabet = dict(
        a='alpha',
        b='bravo',
        c='charlie',
        d='delta',
        e='echo',
        f='foxtrot',
        g='golf',
        h='hotel',
        i='india',
        j='juliet',
        k='kilo',
        l='lima',
        m='mike',
        n='november',
        o='oscar',
        p='papa',
        q='quebec',
        r='romeo',
        s='sierra',
        t='tango',
        u='uniform',
        v='victor',
        w='whisky',
        x='x-ray',
        y='yankee',
        z='zulu'
    )

alphabet.update({
        '-': 'hyphen',
        '.': 'full stop',
        ',': 'comma',
        ':': 'colon',
        '0': 'zero',
        '1': 'one',
        '2': 'two',
        '3': 'three',
        '4': 'four',
        '5': 'five',
        '6': 'six',
        '7': 'seven',
        '8': 'eight',
        '9': 'niner'
    })


def translate(s):
    s = s.lower()
    f = []
    o = []
    
    i = 0
    skip = False
    
    for char in s:
        o.append(alphabet.get(char, char))
        i += 1
        
        if i % 4 == 0:
            f.append(o)
            o = []
    
    return '.\t[[slnc 1000]]\n'.join([', '.join(i) for i in f])


if __name__ == '__main__':
    for line in sys.stdin:
        print translate(line)
