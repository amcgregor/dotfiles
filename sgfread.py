#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function

import time
import re
import sys
import os

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
print('\033[H\033[2J', end="")

encoding = sys.getdefaultencoding() if sys.getdefaultencoding() != 'ascii' else 'utf8'
move_re = re.compile('^(W|B)\[([a-t])([a-t])\]');


class Board(object):
    conv = {None: u"·", 'W': u"⚫", 'B': u"⚪"}
    
    def __init__(self, size=19):
        """Initialize the screen and board."""
        self.size = size
        self.array = [[None for y in xrange(size)] for x in xrange(size)]
        self.prisoners = dict(W=0, B=0)
        self.groups = None # TODO: Array of groups, linked list of stones.
        
        for x, row in enumerate(self.array):
            for y, cell in enumerate(self.array):
                if (x in (3, 15) and y in (3, 15)) or (x,y) == (size/2, size/2):
                    print(u'\033[{};{}H\033[8m·\033[0m'.format(*self.to_screen_coord(x, y)).encode(encoding), end="")
                else:
                    print(u'\033[{};{}H·'.format(*self.to_screen_coord(x, y)).encode(encoding), end="")
                # time.sleep(0.01)
        
        print(u"\033[{0};0H{1}×{1} board prepared.".format(size + 1, size).encode(encoding))
        time.sleep(0.5)
    
    def to_screen_coord(self, x, y):
        return y+1, (1 + x) * 2 - 1
    
    @classmethod
    def file(cls, fname):
        with open(fname) as f:
            obj = cls()
            
            for line in f:
                for chunk in line.split(';'):
                    m = move_re.search(chunk)
                    if not m: continue
                    
                    color, x, y = m.group(1), ord(m.group(2)) - 97, ord(m.group(3)) - 97
                    
                    obj.move(x, y, color)
                    
                    print("%s moved at %s,%s" % ('White' if color == 'W' else 'Black', x, y), end="\r")
                    time.sleep(0.2)
        
        return obj

    def remove_if_dead(self, x, y, color, direction=""):
        board = self.array
        
        if x < 0 or x > 18 or y < 0 or y > 18:
            return
    
        group = self.group_at(x, y, color='W' if color == 'B' else 'B')
        
        if group and self.liberties(group) == 0:
            for x, y in group:
                print((u'\033[{};{}H·').format(*self.to_screen_coord(x, y)).encode(encoding), end="")
                self.prisoners[color] += 1
                board[x][y] = None

    
    def move(self, x, y, color):
        board = self.array
        
        board[x][y] = color
        
        if x > 0 and board[x-1][y] != color:
            self.remove_if_dead(x-1, y, color, '<')
        
        if x < self.size - 1 and board[x+1][y] != color:
            self.remove_if_dead(x+1, y, color, '>')
        
        if y > 0 and board[x][y-1] != color:
            self.remove_if_dead(x, y-1, color, '^')
        
        if y < self.size - 1 and board[x][y+1] != color:
            self.remove_if_dead(x, y+1, color, 'v')
        
        print(u'\033[{};{}H{}\033[{};0H\033[2K'.format(*(list(self.to_screen_coord(x, y))+[self.conv[color], self.size+1])).encode(encoding), end="")
    
    def liberties(self, group):
        board = self.array
        liberties = set()
        
        for gr_x, gr_y in group:
            if gr_x > 0 and board[gr_x-1][gr_y] is None:
                liberties.add((gr_x-1, gr_y))
            
            if gr_x < 18 and board[gr_x+1][gr_y] is None:
                liberties.add((gr_x+1, gr_y))
            
            if gr_y > 0 and board[gr_x][gr_y-1] is None:
                liberties.add((gr_x, gr_y-1))
          
            if gr_y < 18 and board[gr_x][gr_y+1] is None:
                liberties.add((gr_x, gr_y+1))
        
        return len(liberties)

    def group_at(self, x, y, color=None, group=None):
        board = self.array
        
        if color is None:
            color = board[x][y]
        
        if group is None:
            group = set()
        
        if not board[x][y] or board[x][y] != color or (x, y) in group:
            return None

        group.add((x, y))
        
        if x > 0:
            self.group_at(x-1, y, color, group)
        
        if x < 18:
            self.group_at(x+1, y, color, group)
        
        if y > 0:
            self.group_at(x, y-1, color, group)
        
        if y < 18:
            self.group_at(x, y+1, color, group)
        
        return group

if __name__ == '__main__':
    board = Board.file(sys.argv[1])
    print("White has %d prisoners" % board.prisoners['W'])
    print("Black has %d prisoners" % board.prisoners['B'])
