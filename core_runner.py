#!/usr/bin/env python

"""Based on the pre-commit hook found on this blog post:

http://tech.yipit.com/2011/11/16/183772396/

Updated to use ack (it's faster, targeted, automatically ignores .git).
Also updated to collapse several checks into one (e.g. pdb/ipdb).
"""

from __future__ import print_function

import os
import pipes
import re
import subprocess
import sys

from shared import colors

# pulled from marrow.util.convert, Copyright (c) 2009-2011 Alice Bevan-McGregor and contributors.
# MIT licensed
def boolean(input):
    try:
        input = input.strip().lower()
    except AttributeError:
        return bool(input)

    if input in ('yes', 'y', 'on', 'true', 't', '1'):
        return True

    if input in ('no', 'n', 'off', 'false', 'f', '0'):
        return False

    raise ValueError("Unable to convert {0!r} to a boolean value.".format(input))

class ANSIColorStripper(object):
    filter = re.compile(r"\033\[\d+(;\d+)*m")
    def write(self, msg):
        sys.__stdout__.write(self.filter.sub('', msg))

# Check if there should be colorful output
colors_enabled = sys.__stdout__.isatty()

# allow env var override
try:
    colors_enabled = boolean(os.environ['COLORFUL'])
except KeyError:
    pass

if not colors_enabled:
    sys.stdout = ANSIColorStripper()

modified = re.compile('^(?:M|A)(\s+)(?P<name>.*)')

ACK_BASE = '''ack --context=1 --color --sort-files '''
PY_BASE = ACK_BASE + '--type=python '
JS_BASE = ACK_BASE + '--type=js '

PY_FILES = lambda name: os.path.splitext(name)[1] == '.py'
JS_FILES = lambda name: os.path.splitext(name)[1] == '.js'


python_checks = [
        dict(
                command='''pyflakes {0}''',
                filter=PY_FILES
            ),
        dict(
                label="pdb/ipdb imports",
                command=PY_BASE + '''"(import i?pdb)|(__import__\(['\\"]i?pdb['\\"]\))" {0} 1>&2''',
                filter=PY_FILES,
                expect=1
            ),
        dict(
                label="encoding declaration",
                command=PY_BASE + '''--files-without-matches --max-count=1 "coding[:=]\s*([-\w.]+)" {0} 1>&2''',
                filter=PY_FILES,
                expect=1
            )
]

CHECKS = []

def run_check(check, files):
    files = ' '.join(map(pipes.quote, filter(check.get('filter', bool), files)))
    
    if not files and "{0}" in check['command']:
        return
    
    cmd = check['command'].format(files)
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = process.communicate()
    
    failed = process.returncode != check.get('expect', 0)
    
    if failed:
        print("   {info}<{r} {0}".format(cmd, **colors))
        
        if out:
            print(("   {warn}>{r} " + "\n   {warn}>{r} ".join(out.strip().splitlines())).format(**colors))
        
        if err:
            print(("   {error}!{r} " + "\n   {error}!{r} ".join(err.strip().splitlines())).format(**colors))
    
    return int(failed)


def main():
    # Stash changes to the working tree that are not part of this commit.
    subprocess.call(['git', 'stash', '-u', '--keep-index'], stdout=subprocess.PIPE)
    
    # Identify files modified in this commit.
    p = subprocess.Popen(['git', 'status', '--porcelain'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    files = [match.group('name') for match in map(modified.match, out.splitlines())]
    
    result = 0
    
    # Run each check.
    for check in CHECKS:
        if 'output' in check:
            print(" {ok}*{r} {0}".format(check['output'], **colors))
        elif 'label' in check:
            print(" {ok}*{r} Checking for {b}{0}{r}".format(check['label'], **colors))
        else:
            print(" {ok}*{r} Running: {b}{0}{r}".format(check['command'].replace('{0}', '').strip(), **colors))

        result = run_check(check, files) or result
    
    # Unstash the changes.
    
    subprocess.call(['git', 'stash', 'pop', '-q', '--index'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    return result
