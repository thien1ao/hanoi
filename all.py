import pygame
import tkinter as tk
from tkinter import ttk
from sys import exit
from colour import Color


def hanoi(n, start, end): 
    """create moeves"""
    if n == 1: moves.append((start,end))
    else:
        other = 6 - (start + end)
        hanoi(n-1, start, other)
        moves.append((start,end))
        hanoi(n-1, other, end)

def startmove(movenum): # remove the top disk from the starting peg and save it to a temp variable
    start = moves[movenum][0]-1
    end = moves[movenum][1]-1
    a = columns[start].pop(-1)
    activedisk = a[0]; activecolor = a[1]
    return start, end, activedisk, activecolor

def drawdisk(width,color,column,level,active=False): # draw a disk on screen
    t = {0:70,1:200,2:330} # x position depends on column
    y = sh-20-(10*level) # y position depends on level
    if active: y += 10*(12-n)
    if coloron: color = color.hex_l # convert color object to hex if necessary
    pygame.draw.rect(screen,color,(t[column]-(width//2),y,width,10))

step = -1 # the current step in a three step move
def nxt(step):
    if step == 3: return 1 # if the move is over, go to the next
    else: return step + 1 # or continue the move

n = 3 # number of disks defaults to 3
mn = 0 # first index in moves list is 0
over = False # state of animation
delay = 201 # artificial delay in ms

def increase(): # increase disks from gui
    n = int(text.get()[-2:])
    n += 1; n = min(n,12)
    text.set('Disks: '+str(n))  

def decrease(): # decrease disks from gui
    n = int(text.get()[-2:])
    n -= 1; n = max(3,n)
    text.set('Disks: '+str(n))

def kill(): # kill gui
    gui.destroy()

# tk root
gui = tk.Tk()
gui.geometry('660x350')  
gui.title('Tower of Hanoi Config')
gui.option_add('*Font', '20')

text = tk.StringVar()
text.set('Disks: '+str(n))

# color
c = tk.BooleanVar(value=False)

# show number of disks
nlabel = tk.Label(gui, textvariable=text)
nlabel.grid(column=1,row=0,ipady=10)

increasebutton = tk.Button(gui, text=">", command=increase)
increasebutton.grid(column=2,row=0,ipady=10)

decreasebutton = tk.Button(gui, text='<', command=decrease)
decreasebutton.grid(column=0,row=0,ipady=10)

startbutton = tk.Button(gui, text='Start', command=kill)
startbutton.grid(column=1,row=3,ipady=10)

colorbox = tk.Checkbutton(gui,text='Color',variable=c,onvalue=True)
colorbox.grid(column=1,row=2,ipady=10)

gui.mainloop()

# read disks and color toggle
n = int(text.get()[-2:])
coloron = c.get()

pygame.init()

if coloron: red = Color('red'); colors = list(red.range_to(Color('blue'),n)) # creates a list of n colors from red to blue
else: colors = [0xffffff for _ in range(n)] # or make them all white

sw = 400 # screen width
sh = 170-10*(12-n) # screen height
#sh = 170
screen = pygame.display.set_mode((sw,sh)) 

moves = [] # list of moves to solve the hanoi problem
columns = [[],[],[]] # there are three columns, each being a list of disks

for i in range(1,n+1): columns[0].insert(0,(10+10*i,colors[i-1])) # stack n disks on the first column

hanoi(n,1,3) # generate moves

while True:
    screen.fill((50,50,50))
    pygame.display.set_caption(f"Tower of Hanoi | {n} disks | move {mn+1} | {delay-1} ms")
    
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: pygame.quit(); exit()
    
    keys = pygame.key.get_pressed() # change delay on input
    if keys[pygame.K_UP]: delay -= 25
    elif keys[pygame.K_DOWN]: delay += 25
    delay = max(1,min(delay,1001))

    # draw columns
    pygame.draw.rect(screen,(255,255,255),(0,sh-10,sw,10))
    pygame.draw.rect(screen,(255,255,255),(65,sh-140+10*(12-n),10,sh))
    pygame.draw.rect(screen,(255,255,255),(195,sh-140+10*(12-n),10,sh))
    pygame.draw.rect(screen,(255,255,255),(325,sh-140+10*(12-n),10,sh))
    
    step = nxt(step) # next step
    if not over:
        if step == 1: # remove the active disk from the start column and draw it above
            start, end, activedisk, activecolor = startmove(mn)
            drawdisk(activedisk,activecolor,start,14,True)
        elif step == 2: # then draw the active disk above the end column
            drawdisk(activedisk,activecolor,end,14,True)
        elif step == 3: # then add the active disk to the end column
            columns[end].append((activedisk,activecolor))
    
    if step == 3 and not over: # go to next move after 3 steps
        mn += 1
        if mn == len(moves): over = True; mn -= 1 # stop if no more moves
    
    for col, column in enumerate(columns): # draw all disks besides the active one
        for level,disk in enumerate(column): drawdisk(disk[0],disk[1],col,level)
    
    pygame.display.update()
    pygame.time.delay(delay)