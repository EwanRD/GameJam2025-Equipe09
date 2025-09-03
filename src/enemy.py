import pygame
from pygame.locals import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y,human):
        super().__init__()
        self.human = human
        self.image = pygame.Surface([50,45])
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.score = 0
  
        self.rect.x = 400
        self.rect.y = 40
  
        self.change_x = 0
        self.change_y = 0
        self.walls = None
  
    def changespeed(self,x,y):
        self.change_x += x
        self.change_y += y
  
    def update(self):
        if self.human.rect.x > self.rect.x :
            self.rect.x += 1
        if self.human.rect.x < self.rect.x :
            self.rect.x -= 1
        if self.human.rect.y > self.rect.y :
            self.rect.y += 1
        if self.human.rect.y < self.rect.y :
            self.rect.y -= 1
