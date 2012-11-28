# encoding: utf-8

from textwrap import wrap


def wrap(text, columns=78):
    lines = []
    for iline in text.splitlines():
        if not iline:
            lines.append(iline)
        else:
            for oline in wrap(iline, columns):
                lines.append(oline)
    
    return "\n".join(lines)
