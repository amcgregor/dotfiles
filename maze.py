# encoding: utf-8

myMap = [[1, 1, 1, 1, 1, 1, 1, 1],
         [1, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 1, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 1, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 1],
         [1, 1, 1, 1, 1, 1, 1, 1]]


class GameObject(object):
    myMap = myMap
    _xSpeed = 0
    _ySpeed = 0
    _x = 1
    _y = 1
    _shape = ""
    
    def print_map(self):
        print "\033[2J\033[1;1H"
        
        for row in range(len(self.myMap)):
            for col in range(len(self.myMap[row])):
                print self._shape if (row, col) == (self._y, self._x) else ("#" if self.myMap[row][col] else " "),
            
            print
    
    def collision(self):
        if self.myMap[self._y + self._ySpeed][self._x + self._xSpeed]:
            return True
        else: return False
    
    def move(self):
        if self._xSpeed != 0 or self._ySpeed != 0:
            if not self.collision():
                self._x += self._xSpeed
                self._y += self._ySpeed
        self._xSpeed = 0
        self._ySpeed = 0


class Player(GameObject):
    _shape = "@"
    
    def handle_key(self, keychar):
        #MOVEMENT
        if keychar == "e":
            self._xSpeed = 1
        elif keychar == "w":
            self._xSpeed = -1
        elif keychar == "n":
            self._ySpeed = -1
        elif keychar == "s":
            self._ySpeed = 1


if __name__ == '__main__':
    player = Player()
    
    while True:
        player.print_map()
        direction = raw_input("\nEnter Direction [nsweq]: ").strip()
        if direction == "q": break
        player.handle_key(direction)
        player.move()
    