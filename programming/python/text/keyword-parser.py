#!/usr/bin/env python
# encoding: utf-8

import re


class KeywordProcessor(object):
    """Process user-supplied keywords, tags, or search terms.
    
    This tries to be as flexible as possible while being efficient.
    The vast majority of the work is done in the regular expression."""
    
    def __init__(self, separators=' \t', quotes=['"', "'"], groups=[], group=False, normalize=None, sort=False, result=list):
        """Configure the processor.
        
        separators: A list of acceptable separator characters.  The first will be used for joins.
        quotes: Pass a list or tuple of allowable quotes. E.g. ["\"", "'"] or None to disable.
        groups: Pass a string, list, or tuple of allowable prefixes.  E.g. '+-' or None to disable.
        group: Pass in the type you want to group by, e.g. list, tuple, or dict.
        normalize: Pass a function which will normalize the results.  E.g. lambda s: s.lower().strip(' \"')
        sort: Sort the resulting list (or lists) alphabeticlly.
        result: The return type.  One of set, tuple, list.
        
        If groups are defined, and group is not, the result will be a list/tuple/set of tuples, e.g. [('+', "foo"), ...]
        """
        
        separators = list(separators)
        
        self.pattern = ''.join((
                ('[\s%s]*' % (''.join(separators), )), # Trap possible leading space or separators.
                '(',
                    ('[%s]%s' % (''.join([i for i in list(groups) if i is not None]), '?' if None in groups else '')) if groups else '', # Pass groups=('+','-') to handle optional leading + or -.
                    ''.join([(r'%s[^%s]+%s|' % (i, i, i)) for i in quotes]) if quotes else '', # Match any amount of text (that isn't a quote) inside quotes.
                    ('[^%s]+' % (''.join(separators), )), # Match any amount of text that isn't whitespace.
                ')',
                ('[%s]*' % (''.join(separators), )), # Match possible separator character.
            ))
        self.regex = re.compile(self.pattern)
        
        self.groups = list(groups)
        self.group = dict if group is True else group
        self.normalize = normalize
        self.sort = sort
        self.result = result
    
    def split(self, value):
        if not isinstance(value, basestring): raise TypeError("Invalid type for argument 'value'.")
        
        matches = self.regex.findall(value)
        
        if callable(self.normalize): matches = [self.normalize(i) for i in matches]
        if self.sort: matches.sort()
        if not self.groups: return self.result(matches)
        
        groups = dict([(i, list()) for i in self.groups])
        if None not in groups.iterkeys(): groups[None] = list() # To prevent errors.
        
        for i in matches:
            if i[0] in self.groups:
                groups[i[0]].append(i[1:])
            else:
                groups[None].append(i)
        
        if self.group is dict: return groups
        
        if self.group is False or self.group is None:
            results = []
            
            for group in self.groups:
                results.extend([(group, match) for match in groups[group]])
            
            return self.result(results)
        
        return self.group([[match for match in groups[group]] for group in self.groups])


if __name__ == '__main__':
    tag_parser = KeywordProcessor(' \t,', normalize=lambda s: s.lower().strip('"'), sort=True, result=tuple)
    search_parser = KeywordProcessor(groups=[None, '+', '-'], group=tuple)
    
    print "Tag Parser Regex:", repr(tag_parser.pattern)
    print "Search Parser Regex:", repr(search_parser.pattern)
    
    print
    
    def test_search(s):
        print "Parse Search:", s
        print "Parse Result:", search_parser.split(s)
        print
    
    _ = '"high altitude" "melting panda" panda bends'
    print "Parse Tags:", _
    print "Parse Result:", tag_parser.split(_)
    
    print
    
    test_search('animals +cat -dog +"medical treatment"')
    test_search('animal medicine +cat +"kitty death"')
    
    search_parser.group = dict
    test_search(' foo  bar "baz"diz       ')
    test_search('cat dog -leather')
    
    # Test unicode...
    print tag_parser.split('© 2009')
