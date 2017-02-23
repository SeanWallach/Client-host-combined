# Sean Wallach Grade 12 Comp sci
# 1/25/2016
# Version 1.5
# known issues: -sometimes at init. x cords and y cords received will be swapped or combined and the program may crash.
#               -lots of lag when moving characters. I believe its from not having enough time to detect keypresses

import pygame, sys, time, socket, ctypes
from pygame.locals import *

while 1 == 1:
    hoc = input("Are you host or client? (h/c)")    #figuring which main loop to run (host or client)
    if hoc == "h":  #if host
        s = socket.socket()             #setting up server
        host = socket.gethostname()     #
        port = 12345                    #
        try:                                        
            s.bind((host, port))
            print('Server up.')
            s.listen(5)
            t= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)             #getting your ip
            t.connect(("gmail.com",80))                                     #
            print("Waiting for connection... your ip: ",t.getsockname()[0]) #
            t.close()                                                       #
            #accepting connection and running host loop
            c, addr = s.accept()                                                    
            print("Got connection from " + str(addr[0]) + ' : ' + str(addr[1]))
            flag = 1
            break
        except:
            print("An error has occured. Maybe the port is occupied.")
    elif hoc == "c":                        #if client
        s = socket.socket()            
        host = input("What is the host ip? ")      
        port= 12345                     
        try:
            s.connect((host, port))         #connecting to host and running client loop
            print('Connected to host.')
            flag = 2
            break
        except:
            print("An error has occured, try typing a valid address or making sure the host is live.")      
    else:
        print("Not a valid response, try again.")
        
#pygame initialize
pygame.init()
FPS=30
fpsClock=pygame.time.Clock()

#finding screensize and loading some background stuff
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
DISPLAYSURF=pygame.display.set_mode(screensize,pygame.FULLSCREEN)
pygame.display.set_caption('Animation')
background=pygame.image.load('back.jpg')

UP='up'
LEFT='left'
RIGHT='right'
DOWN='down'

#sprite init
S_sprite=pygame.image.load('host.png')
S_spritex=200
S_spritey=130

C_sprite=pygame.image.load('client.png')
C_spritex=600
C_spritey=130

DISPLAYSURF.blit(S_sprite,(S_spritex,S_spritey))
DISPLAYSURF.blit(C_sprite,(C_spritex,C_spritey))

if flag == 1:
    while True:
        DISPLAYSURF.blit(background,(0,0))
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
        if event.type == KEYDOWN:           #movement
            if (event.key == K_LEFT):
                S_spritex-=5               
            elif (event.key == K_RIGHT):
                S_spritex+=5
            elif (event.key == K_UP):
                S_spritey-=5
            elif (event.key == K_DOWN):
                S_spritey+=5

        #converting and sending coordinates 
        S_spritex = str(S_spritex)
        S_spritey = str(S_spritey)          
        c.send(bytes(S_spritex,'UTF-8'))
        c.send(bytes(S_spritey,'UTF-8'))
        S_spritex = int(S_spritex)
        S_spritey = int(S_spritey)

        #reading messages that are received
        message = (c.recv(1024).decode())
        C_spritex = int(message)
        print("x cord: ", message)
        message = (c.recv(1024).decode())
        C_spritey = int(message)
        print("y cord: ", message)
        DISPLAYSURF.blit(S_sprite,(S_spritex,S_spritey))
        DISPLAYSURF.blit(C_sprite,(C_spritex,C_spritey))
        pygame.display.update()
        fpsClock.tick(FPS)   
if flag == 2:
    while True:
        DISPLAYSURF.blit(background,(0,0))
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
        if event.type == KEYDOWN:
            if (event.key == K_LEFT):
                C_spritex-=5               
            elif (event.key == K_RIGHT):
                C_spritex+=5
            elif (event.key == K_UP):
                C_spritey-=5
            elif (event.key == K_DOWN):
                C_spritey+=5

        #converting and sending coordinates
        C_spritex = str(C_spritex)
        C_spritey = str(C_spritey)
        s.send(bytes(C_spritex,'UTF-8'))
        s.send(bytes(C_spritey,'UTF-8'))
        C_spritex = int(C_spritex)
        C_spritey = int(C_spritey)

        #reading messages that are received 
        message = (s.recv(1024).decode())       
        S_spritex = int(message)
        print("x cord: ", message)
        message = (s.recv(1024).decode())
        S_spritey = int(message)
        print("y cord: ", message)
        DISPLAYSURF.blit(C_sprite,(C_spritex,C_spritey))
        DISPLAYSURF.blit(S_sprite,(S_spritex,S_spritey))
        pygame.display.update()
        fpsClock.tick(FPS)   
