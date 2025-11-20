import pygame as pg
from pygame import sprite as spr
from random import randint, random

import constants as k

pg.init()
pg.display.set_mode(k.SCREENSIZE)

class Spritecut:
    def __init__(self, filename, num_per_row, rows, wide, high, left_border = 0, top_border = 0, h_gap = 0, v_gap = 0):
        self.imagelist = []
        self.b_width = wide
        self.b_high = high
        self.image_count = num_per_row * rows
        # get the sheet of sprites
        self.sheet = pg.image.load(filename).convert_alpha()
        # loop through each row to get the images from that row
        for j in range (rows):
            for i in range (num_per_row):
                startx = left_border + (i * (self.b_width + h_gap))
                starty = top_border + (j * (self.b_high + v_gap))
                rect = pg.Rect(startx, starty, self.b_width, self.b_high)
                self.imagelist.append(self.get_sprite(rect))
    def get_sprite(self,rect):
        a_image = pg.Surface((self.b_width, self.b_high),pg.SRCALPHA).convert_alpha()
        a_image.blit(self.sheet,(0,0),rect)
        return a_image
    def show_sprite(self,number):
        return self.imagelist[number]

ballsheet = Spritecut("sprites.png",1,1,50,50,100,0)
barsheet = Spritecut("sprites.png",2,1,40,150,5,0,10)

def randomspeed(a,b,A=k.BSPX,B=k.BSPY):
    x = randint(a,A)
    if random() < 0.5:
        x = -x
    y = randint(b,B)
    if random() < 0.5:
        y = -y
    return (x,y)

class Ball(spr.Sprite):
    centerx = k.SCREENWIDE/2-ballsheet.b_width/2
    centery = k.SCREENHIGH/2-ballsheet.b_high/2
    def __init__(self):
        spr.Sprite.__init__(self, self.containers)
        self.image = ballsheet.show_sprite(0)
        self.speed = self.x, self.y = randomspeed(5,3)
        self.diameter = ballsheet.b_width
        self.rect = self.image.get_rect()
        self.radius = k.BALLDIAM/2
        self.rect.x = self.centerx
        self.rect.y = self.centery

    def reset(self):
        self.rect.x = self.centerx
        self.rect.y = self.centery
        self.speed = self.x, self.y = randomspeed(5, 3)

    def update(self, *args, **kwargs):
        self.rect = self.rect.move(self.speed)
        # top or bottom, reverse y direction
        if self.rect.top < 0 or self.rect.bottom > k.SCREENHIGH:
            self.y = -self.y
            self.speed = (self.x,self.y)


class Paddle(spr.Sprite):
    speed = k.PADDLESPEED
    def __init__(self,paddlesideleftTrue):
        spr.Sprite.__init__(self, self.containers)
        self.wide = barsheet.b_width
        self.high = barsheet.b_high
        if paddlesideleftTrue:
            self.image = barsheet.show_sprite(0)
            self.startx = 25
        else:
            self.image = barsheet.show_sprite(1)
            self.startx = k.SCREENWIDE - barsheet.b_width - 25
        self.starty = k.SCREENHIGH/2 - barsheet.b_high/2
        self.rect = self.image.get_rect()
        #self.rect.width = k.PADDLETHICKNESS
        self.rect.x = self.startx
        self.rect.y = self.starty

    def move(self,direction):
        self.rect.move_ip(0,direction*self.speed)