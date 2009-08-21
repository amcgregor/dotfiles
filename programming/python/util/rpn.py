#!/usr/bin/env python
# encoding: utf-8
"""
rpn.py

Created by Alice Bevan–McGregor on 2009-08-18.
Copyright (c) 2009 Alice Bevan-McGregor. All rights reserved.

Released under an MIT license.  You can find a copy somewhere.
"""

import sys
import getopt

from decimal import *


help_message = '''
A simple command line based RPN calculator.
'''


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg



class StackArgs(object):
    def __init__(self, count):
        self.count = count
    
    def __call__(self, fn):
        this = self
        
        def wrapper(self):
            args = []
            
            if this.count > 0:
                args = self[-this.count:]
                del self[-this.count:]
            
            self.append(fn(self, *args))
            return self[-1]
        
        wrapper.arguments = self.count
        
        return wrapper
    
    
args = StackArgs


class RPN(list):
    def __init__(self, *args, **kw):
        super(RPN, self).__init__(*args, **kw)
    
    def enter(self, value):
        self.append(value)
    
    @args(2)
    def max(self, a, b): return a.max(b)
    
    @args(2)
    def min(self, a, b): return a.min(b)
    
    @args(1)
    def sqrt(self, a): return a.sqrt()
    
    @args(1)
    def abs(self, a): return getcontext().abs(a)
    
    @args(2)
    def add(self, a, b): return a + b
    
    @args(2)
    def subtract(self, a, b): return a - b
    
    @args(2)
    def multiply(self, a, b): return a * b
    
    mul = multiply
    
    @args(2)
    def divide(self, a, b): return a / b
    
    div = divide
    
    @args(2)
    def exponent(self, a, b): return a ** b
    
    @args(2)
    def modulus(self, a, b): return a % b
    
    mod = modulus
    
    @args(1)
    def sin(self, a):
        """Return the sine of x as measured in radians.
        
        >>> print sin(Decimal('0.5'))
        0.4794255386042030002732879352
        >>> print sin(0.5)
        0.479425538604
        >>> print sin(0.5+0j)
        (0.479425538604+0j)
        
        """
        getcontext().prec += 2
        i, lasts, s, fact, num, sign = 1, 0, a, 1, a, 1
        while s != lasts:
            lasts = s    
            i += 2
            fact *= i * (i-1)
            num *= a * a
            sign *= -1
            s += num / fact * sign 
        getcontext().prec -= 2        
        return +s
    
    @args(1)
    def cos(self, a):
        """Return the cosine of x as measured in radians.

        >>> print cos(Decimal('0.5'))
        0.8775825618903727161162815826
        >>> print cos(0.5)
        0.87758256189
        >>> print cos(0.5+0j)
        (0.87758256189+0j)

        """
        getcontext().prec += 2
        i, lasts, s, fact, num, sign = 0, 0, 1, 1, 1, 1
        while s != lasts:
            lasts = s    
            i += 2
            fact *= i * (i-1)
            num *= a * a
            sign *= -1
            s += num / fact * sign 
        getcontext().prec -= 2        
        return +s
    
    @args(0)
    def pi(self, *args):
        """Compute Pi to the current precision.

        >>> print pi()
        3.141592653589793238462643383

        """
        getcontext().prec += 2  # extra digits for intermediate steps
        three = Decimal(3)      # substitute "three=3.0" for regular floats
        lasts, t, s, n, na, d, da = 0, three, 3, 1, 0, 0, 24
        while s != lasts:
            lasts = s
            n, na = n+na, na+8
            d, da = d+da, da+32
            t = (t * n) / d
            s += t
        getcontext().prec -= 2
        return +s               # unary plus applies the new precision
    
    
    mapping = {
            '+': add,
            '-': subtract,
            '*': multiply,
            '/': divide,
            '^': exponent,
            '%': modulus,
            'sin': sin,
            'cos': cos,
            'pi': pi,
            'min': min,
            'max': max,
            'sqrt': sqrt,
            'abs': abs,
            
        }


def main(argv=None):
    if argv is None: argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h:v", ["help"])
        
        except getopt.error, msg:
            raise Usage(msg)
        
        # option processing
        for option, value in opts:
            if option == "-v":
                verbose = True
            if option in ("-h", "--help"):
                raise Usage(help_message)
        
        calculator = RPN()
        
        # Expand any string lists.
        
        nargs = []
        for i in args:
            if ' ' in i: nargs.extend(i.split(' '))
            else: nargs.append(i)
        
        args = nargs
        del nargs
        
        # Process the arguments and calculate.
        for i in args:
            # print '#', i
            
            if i in calculator.mapping:
                print i, '\t', calculator.mapping[i](calculator)
                continue
            
            calculator.append(Decimal(i))
            print ' ', '\t', i
        
        # return int(calculator.pop())
    
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
