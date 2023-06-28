import pygame
from constantes import *

class Player():
    def __init__(self, x, y, speed = 15, jump = 4)->None:
        self.x = x
        self.y = y
        self.speed = speed
        self.jump_height = jump
        self.size_x = TAM_X_JUGADOR
        self.size_y = TAM_Y_JUGADOR
        

    def control(self, accion:str, display):
        """Movimientos basicos del jugador
        GO_LEFT = desplazamiento izquierda
        GO_RIGHT = desplazamiento derecha
        JUMP = desplazamiento arriba
        GO_DOWN = desplazamiento abajo



        Args:
            accion (str): movimiento a realizar
            display (pygame.display): pantalla sobre la cual realizar el movimiento
        """
        match accion:
            case "GO_LEFT":
                self.x -= self.speed
            case "GO_RIGHT":
                self.x += self.speed
            case "JUMP":
                self.y -= self.speed
                if self.y < 0:
                    self.y = 0
            case "GO_DOWN":
                self.y += self.speed
                if self.y > Y_PISO_BASE:
                    self.y = Y_PISO_BASE
            case _:
                pass
        print("pos: {0},{1}".format(self.x,self.y))


    def update_position(self,display)->None:
        pygame.draw.rect(display, (255,0,0),(self.x,self.y, self.size_x, self.size_y))

