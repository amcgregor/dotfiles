# -*- coding: utf-8 -*-

import re


escapes = re.compile(r'(\\[^\\]\([^\)]+\)|\\[^\\]|\\\\|%[^%][\w]?|%%|\$\([^\)]+\)|\$\$)')

escape_slashes = {
        # Basic symbols.
        't': "\t", # Tab
        'n': "\n", # Newline
        'r': "\r", # Carriage Return
        
        # Color codes.
        
        's(normal)': "\033[0m",
        
        's(bold)': "\033[1m",
        's(intense)': "\033[1m",
        's(dim)': "\033[2m",
        's(italic)': "\033[3m",
        's(underline)': "\033[4m",
        's(inverse)': "\033[7m",
        's(hidden)': "\033[8m",
        's(strike)': "\033[9m",
        
        'c(black)': "\033[30m",
        'c(red)': "\033[31m",
        'c(green)': "\033[32m",
        'c(yellow)': "\033[33m",
        'c(blue)': "\033[34m",
        'c(magenta)': "\033[35m",
        'c(cyan)': "\033[36m",
        'c(white)': "\033[37m",
        'c(default)': "\033[39m",
        
        'b(black)': "\033[40m",
        'b(red)': "\033[41m",
        'b(green)': "\033[42m",
        'b(yellow)': "\033[43m",
        'b(blue)': "\033[44m",
        'b(magenta)': "\033[45m",
        'b(cyan)': "\033[46m",
        'b(white)': "\033[47m",
        'b(default)': "\033[49m"
    }

escape_percents = dict(t="\t", r="\n", b=' ')
# %xN - h=highlight - n=normal - f=flashing - u=underline - i=invert - 

#escape_slash_function['c(rainbow)'] - Rotate through all 16 colors.
#escape_slash_function['c(stripe)'] - Alternate between highlight and normal.
#escape_slash_function['c(duotone'] - Alternate between two colors passed as comma-separated escapes.

local_percents_base = dict(
        s = dict(m="he", f="she", i="it", g="they"),        # subjective: he, she, it, they
        o = dict(m="him", f="her", i="it", g="them"),       # objective: him, her, it, them
        p = dict(m="his", f="her", i="its", g="their"),     # posessive: his, her, its, their
        a = dict(m="his", f="hers", i="its", g="theirs"),   # absolute posessive: his, hers, its, theirs
    )

for i in ('s', 'o', 'p', 'a'):
    local_percents_base[i.upper()] = dict([(i, j.title()) for i, j in local_percents_base[i].iteritems()])


def unescape(caller, text, obj=None):
    gender = caller.properties.get('sex', 'i')[0] if caller else 'i'
    
    local_slashes = dict()
    
    local_percents = dict([(i, j[gender]) for i, j in local_percents_base.iteritems()])
    local_percents.update({
            'N': caller.name if caller else 'Anonymous',
            'l': ("#%d" % ( caller.location.id, )) if caller else '%l',
            'c': caller.properties['__last_command'] if caller and '__last_command' in caller.properties else '%c',
            '#': ("#%d" % ( caller.id, )) if caller else '%#',
            '@': ("#%d" % ( caller.id, )) if caller else '%#'
        })
    
    def process(match):
        match = match.group(0)
        
        if match == '\\\\': return "\\"
        elif match == '%%': return '%'
        elif match == '$$': return '$'
        
        if match.startswith('\\') and match[1:] in escape_slashes: return escape_slashes[match[1:]]
        if match.startswith('%') and match[1:] in escape_slashes: return escape_slashes[match[1:]]
        
        if match.startswith('\\') and match[1:] in local_slashes: return local_slashes[match[1:]]
        if match.startswith('%') and match[1:] in local_percents: return local_percents[match[1:]]
        
        if match.startswith('$(') and match.endswith(')') and obj:
            match = match[2:-1].split('.')
            ref = obj
            for i in match:
                ref = getattr(ref, i, None)
            return unescape(caller, str(ref), obj)
        
        return match
    
    return escapes.sub(process, text)
