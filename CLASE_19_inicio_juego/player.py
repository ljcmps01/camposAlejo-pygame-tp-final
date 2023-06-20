from doctest import FAIL_FAST
import pygame
from constantes import *
from auxiliar import Auxiliar

class Player:
    def __init__(self,x,y,speed_walk,speed_run,gravity,jump) -> None:
        self.walk_r = Auxiliar.getSurfaceFromSpriteSheet("images/caracters/stink/walk.png",15,1)[:12]
        self.walk_l = Auxiliar.getSurfaceFromSpriteSheet("images/caracters/stink/walk.png",15,1,True)[:12]
        self.stay = Auxiliar.getSurfaceFromSpriteSheet("images/caracters/stink/idle.png",16,1)
        self.jump_r = Auxiliar.getSurfaceFromSpriteSheet("images/caracters/stink/jump.png",33,1,False,2)
        self.jump_l = Auxiliar.getSurfaceFromSpriteSheet("images/caracters/stink/jump.png",33,1,True,2)
        self.frame = 0
        self.lives = 5
        self.score = 0
        self.move_x = x
        self.move_y = y
        self.speed_walk =  speed_walk
        self.speed_run =  speed_run
        self.gravity = gravity
        self.jump = jump
        self.animation = self.stay
        self.image = self.animation[self.frame]
        self.rect = self.image.get_rect()

        self.is_jump = False


    def control(self,action):

        if(action == "WALK_R"):
            self.move_x = self.speed_walk
            self.animation = self.walk_r
            self.frame = 0
        elif(action == "WALK_L"):
            self.move_x = -self.speed_walk
            self.animation = self.walk_l
            self.frame = 0
        elif(action == "JUMP_R"):
            self.move_y = -self.jump
            self.move_x = self.speed_walk
            self.animation = self.jump_r
            self.frame = 0
            self.is_jump = True

        elif(action == "JUMP_L"):
            self.move_y = self.jump
            self.animation = self.jump_l
            self.frame = 0
            self.is_jump = True

        elif(action == "STAY"):
            self.animation = self.stay
            self.move_x = 0
            self.move_y = 0
            self.frame = 0
            

    def update(self):
        if(self.frame < len(self.animation) - 1):
            self.frame += 1 
        else: 
            self.frame = 0
            if(self.is_jump == True):
                self.is_jump = False
                self.move_y = 0

        self.rect.x += self.move_x
        self.rect.y += self.move_y
        
        if(self.rect.y < 500):
            self.rect.y += self.gravity
    
    def draw(self,screen):
        self.image = self.animation[self.frame]
        screen.blit(self.image,self.rect)
        


