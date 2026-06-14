# snake game using oop
"""
this is my new snake.py attempt, coming back after quite some time
i dont rly remember what i was gonna do, but i imma try anyway
"""

import random
from copy import deepcopy
import keyboard # requires sudo # had to change vsc's python to the ./.venv/bin/python one
import time

def sgn(x:int)->int:
    """return the sign of an int: -1, 0, 1"""
    return 0 if not x else x//abs(x)

def checkTabAtXY(tab:list[list[int]],x:int,y:int)->None:
    try:
        if tab[x][y]>=0 and list(map(sgn,[tab[x][y-1],tab[x+1][y],tab[x][y+1],tab[x-1][y]])).count(-1)>2:
            tab[x][y]-=2
            checkTabAtXY(tab,x,y+1)
            checkTabAtXY(tab,x+1,y)
            checkTabAtXY(tab,x,y-1)
            checkTabAtXY(tab,x-1,y)
    except: pass

def d7n(X0orY1:int,c0:int)->str:
    if X0orY1%2:
        return 'w' if sgn(c0)>0 else 's'
    return 'd' if sgn(c0)>0 else 'a'

class Mapa:
    hei: int # HEIght of the map
    wid: int # WIDth of the map
    nap: int # Number of APples
    tab: list[list[int]] # game TABle
    def __init__(self,hei,wid,nap):
        self.hei = hei
        self.wid = wid
        self.nap = nap
        self.tab = [[0 for y in range(hei)] for x in range(wid)]
    def gen1stApples(self,snake,o_snakes):
        for i in range(self.nap):
            self.genNewApple(snake,o_snakes)
    def genNewApple(self,snake:list[tuple[int,int]],o_snakes:list[Snake]):
        """takes list of elements of snake's body AND list of other snakes"""
        point=(random.randrange(self.wid),random.randrange(self.hei))
        while point in snake or point in [_1 for _2 in [o_snake.body for o_snake in o_snakes] for _1 in _2] or self.tab[point[0]][point[1]]==1:
            point=(random.randrange(self.wid),random.randrange(self.hei))
        self.tab[point[0]][point[1]] = 1
    def remApple(self,x:int,y:int):
        """removes an apple at X,Y"""
        self.tab[x][y]=0

class Snake:
    body: list[tuple[int,int]] # list of elements of snake's body
    mapa: Mapa # snake's map
    head: str # HEADing
    dead: bool = False
    def __init__(self, startingBody: list[tuple[int,int]], mapa: Mapa, heading: str):
        self.body = startingBody
        self.mapa = mapa
        self.head = heading
    def nextPosition(self)->tuple[int,int]:
        """returns the position at which the snake is going to be the next tick"""
        x,y = self.body[-1]
        if self.head == 'w': y-=1
        elif self.head == 's': y+=1
        elif self.head == 'a': x-=1
        else: x+=1
        return (x,y)
    def isEating(self)->bool:
        if self.dead:
            return False
        x,y=self.nextPosition()
        if self.mapa.tab[x][y] == 1:
            return True
        return False
    def checkIfDead(self, o_snakes:list[Snake])->None:
        """checks if snake is dead and saves it in self.dead"""
        x,y = self.nextPosition()
        wid = self.mapa.wid
        hei = self.mapa.hei
        if 0<=x<wid and 0<=y<hei and (x,y) not in self.body:
            for o_snake in o_snakes:
                if not o_snake.dead:
                    try:
                        o_body = o_snake.body if o_snake.isEating() else o_snake.body[1:]
                    except:
                        o_body = o_snake.body
                    if (x,y) in o_body:
                        self.dead = True
                        return
                    if o_snake.nextPosition() == (x,y):
                        self.dead = True
                        return
                else:
                    if (x,y) in o_snake.body:
                        self.dead = True
                        return
            self.dead = False
            return
        self.dead = True
    def move(self,o_snakes:list[Snake]):
        if self.isEating():
            self.mapa.remApple(*self.nextPosition())
            self.body.append(self.nextPosition())
            self.mapa.genNewApple(self.body,o_snakes)
        else:
            del self.body[0]
            self.body.append(self.nextPosition())
    def setHeading(self, o_snakes:list[Snake])->None:
        """finds best move for opposing snakes and sets their heading to such. 2nd attempt. this is the core of so-called AI"""
        starting_heading = self.head
        prefDir = ""
        tab = deepcopy(self.mapa.tab)
        hx,hy=self.body[-1]
        tab = [[-2 for x in range(self.mapa.wid+2)],*[[-2, *y, -2] for y in tab],[-2 for x in range(self.mapa.wid+2)]]
        for o_s in o_snakes:
            try:
                o_b = [*o_s.body,o_s.nextPosition()] if o_s.isEating() else [*o_s.body[1:],o_s.nextPosition()]
            except:
                o_b = [*o_s.body,o_s.nextPosition()]
            for el in o_b:
                x,y=el[0]+1,el[1]+1
                tab[x][y]-=2
        for el in self.body[:-1]:
            x,y=el[0]+1,el[1]+1
            tab[x][y]-=2
        surrounding1 = [tab[hx+1][hy],tab[hx+2][hy+1],tab[hx+1][hy+2],tab[hx][hy+1]]
        minus2everywhere = sum(surrounding1)==-8
        for x in range(1,self.mapa.wid+1):
            for y in range(1,self.mapa.hei+1):
                checkTabAtXY(tab,x,y)
        surrounding2 = [tab[hx+1][hy],tab[hx+2][hy+1],tab[hx+1][hy+2],tab[hx][hy+1]]
        applesRel:list[tuple[int,int]]=[]
        for x in range(1,self.mapa.wid+1):
            for y in range(1,self.mapa.hei+1):
                if tab[x][y]==1:
                    applesRel.append((x-hx-1,hy-y+1))
        try:
            closestA = min(applesRel,key=lambda a: a[0]**2+a[1]**2)
            cc = 1 if abs(closestA[1])<abs(closestA[0]) else 0 # closer coordinate
            if closestA[cc]:
                prefDir+=d7n(cc,closestA[cc])
            prefDir+=d7n(cc-1,closestA[cc-1])
        except:
            prefDir = ""
        finalDirection = starting_heading
        surrounding = surrounding1 if minus2everywhere else surrounding2
        for d in prefDir+'wasd':
            if surrounding['wdsa'.index(d)]>=0:
                finalDirection=d
                break
        self.head=finalDirection

def printFrame(snake:Snake,o_snakes:list[Snake]):
    wid = snake.mapa.wid
    head = snake.head
    tab = deepcopy(snake.mapa.tab)
    body = snake.body
    for el in body[:-1]:
        tab[el[0]][el[1]] = 2 # snake's body
    tab[body[-1][0]][body[-1][1]] = head # snake's head
    for o_snake in o_snakes:
        for el in o_snake.body[:-1]:
            tab[el[0]][el[1]] = 4 # other snakes' bodies
        tab[o_snake.body[-1][0]][o_snake.body[-1][1]] = o_snake.head.upper() # other snakes' heads

    tab = list(zip(*tab))
    frame = f'\r{" "*20}\r\x1b[{myMapa.hei+2}A'+"##"*(wid+2)+'\n'
    for yLayer in tab:
        lay = [str(x) for x in yLayer]
        lay = ''.join(lay)
        lay=lay.replace("0","  ")
        lay=lay.replace("1","\x1b[1;31m()\x1b[0m")
        lay=lay.replace("2","\x1b[1;32m[]\x1b[0m")
        lay=lay.replace("w","\x1b[1;31mY \x1b[0m")
        lay=lay.replace("s","\x1b[1;31m^ \x1b[0m")
        lay=lay.replace("a","\x1b[1;31m>-\x1b[0m")
        lay=lay.replace("d","\x1b[1;31m-<\x1b[0m")
        lay=lay.replace("4","\x1b[1;33m[]\x1b[0m")
        lay=lay.replace("W","\x1b[1;35mY \x1b[0m")
        lay=lay.replace("S","\x1b[1;35m^ \x1b[0m")
        lay=lay.replace("A","\x1b[1;35m>-\x1b[0m")
        lay=lay.replace("D","\x1b[1;35m-<\x1b[0m")
        frame+="##"+lay+"##\n"
    print(frame+"##"*(wid+2))

def getStartingInfo()->list[int]:
    try:
        wid = int(input("Map's width (default=10): "))
        wid = abs(wid)*wid//wid
    except:
        wid = 10
    try:
        hei = int(input("Map's height (default=10): "))
        hei = abs(hei)*hei//hei
    except:
        hei = 10
    try:
        nap = int(input("Number of apples on the map (default=1): "))
        nap = abs(nap)*nap//nap
    except:
        nap = 1
    return [hei,wid,nap]

def getAiSnakeInfo()->int:
    try:
        ans = int(input("Number of AI opponents (default=0): "))
        ans = abs(ans)*ans//ans
        if ans > 3: ans = 3
    except:
        ans = 0
    return ans

def pressedKeys()->set:
    ret = set()
    if keyboard.is_pressed('left'): ret.add('a')
    elif keyboard.is_pressed('right'): ret.add('d')
    elif keyboard.is_pressed('up'): ret.add('w')
    elif keyboard.is_pressed('down'): ret.add('s')
    return ret

def checkIfWon(arg:list[Snake]|Snake)->bool:
    """takes list if AI or mySnake if not, returns True if the player has won"""
    if type(arg)==Snake:
        if len(arg.body)+arg.mapa.nap == arg.mapa.hei*arg.mapa.wid:
            return True
        return False
    else:
        for s in arg:
            if not s.dead:
                return False
        return True

## setup ###
info = getStartingInfo()
AI = getAiSnakeInfo()
myMapa = Mapa(*info)
mySnake = Snake([(1,1),(2,1),(3,1)],myMapa,'d')
opponentSnakes:list[Snake]=[]
for i in range(AI):
    opponentSnakes.append(Snake([[(myMapa.wid-2,myMapa.hei-2),(myMapa.wid-3,myMapa.hei-2),(myMapa.wid-4,myMapa.hei-2)],[(myMapa.wid-2,1),(myMapa.wid-2,2),(myMapa.wid-2,3)],[(2,myMapa.hei-2),(2,myMapa.hei-3),(2,myMapa.hei-4)]][i],myMapa,'asw'[i]))
myMapa.gen1stApples(mySnake.body,opponentSnakes)
keys=set()
print('\n'*(myMapa.hei+2))
printFrame(mySnake,opponentSnakes)
### main loop ###
while True:
    for i in range(10):
        time.sleep((.5+.4**len(mySnake.body))/10)
        keys = pressedKeys()-keys
        if len(keys) == 0:
            continue
        mySnake.head = list(keys)[0]
        break
    mySnake.checkIfDead(opponentSnakes)
    if mySnake.dead:
        break
    mySnake.move(opponentSnakes)
    for opponentSnake in opponentSnakes:
        hisRivals = list(set([*opponentSnakes,mySnake])-set([opponentSnake]))
        if opponentSnake.dead: continue
        opponentSnake.setHeading(hisRivals)
        opponentSnake.checkIfDead(hisRivals)
        if opponentSnake.dead: continue
        opponentSnake.move(hisRivals)
    printFrame(mySnake,opponentSnakes)
    if checkIfWon(opponentSnakes if AI else mySnake):
        print(f"\r{' '*20}\nYou won!")
        raise SystemExit
print(f'\r{' '*20}\nGame over! Your lenght: {len(mySnake.body)}')
