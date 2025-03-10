import pygame
import math
from functions import *
from constants import *
from animation import *

class Ammo(object):
    def __init__(self, player, sprite):
        self.type = 0
        self.name = "Ammo"
        self.speed = 1
        self.damage = 1
        self.solid = 0
        self.cooldown = 1000 #MILISECONDS
        self.cd_time = False

        self.x = 1
        self.y = 1
        self.sx = 1
        self.sy = 1

        self.width, self.height = 1, 1

        self.sprite = sprite
        self.width = sprite.get_width()
        self.height = sprite.get_height()

        self.player = player
        self.controller = self.player.controller
        if self.width > self.height:
            self.radius = self.width / 2
        else:
            self.radius = self.height / 2

    def tick(self):
        """Ticks cooldown off the players static ammo objects"""
        if self.cd_time > 0:
            self.cd_time -= self.player.controller.clock.get_time()
        else:
            self.cd_time = 0

    def draw(self):
        self.player.screen.blit(self.sprite, (self.x - self.width/2, self.y-self.height/2))

class Bullet(Ammo):
    def __init__(self, player, speed, damage, width, height, sprite):
        super(Bullet, self).__init__(player, sprite)

        self.x, self.y = player.x, player.y

        self.speed = speed
        self.damage = damage
        self.width, self.height = width, height
        self.sprite = sprite
        self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))
        self.sprite = pygame.transform.rotate(self.sprite, self.player.rotation)

        self.sx = -math.cos(math.radians(self.player.rotation)) * self.speed
        self.sy = math.sin(math.radians(self.player.rotation)) * self.speed

    def update(self):
        """Function triggered every frame for ammo objects in controller.ammo"""
        self.x += self.sx
        self.y += self.sy

        if self.collision():   #Check for and handle current collisions
            pass
        else:   #Only check if self hasn't had any collision with obj or player
            if self.x > SCREEN_SIZE[0] or self.x < 0 or self.y > SCREEN_SIZE[1] or self.y < 0:
                self.controller.ammo.remove(self)

    def collision(self):
        """Detect and handle collisions between the bullet-object and players or WorldObjects"""
        for player in self.controller.agents:
            if player != self.player: # enemy

                if detect_collision(self, player):  # Detect and handle collisions with Players
                    self.controller.ammo.remove(self)
                    player.health -= self.damage
                    Animation(self.player.screen, "explosion", (self.x, self.y), 4)
                    return True  # if collision and cur ammo-object is removed, exit function

        for obj in self.controller.map.objects:  # Detect and handle collisions with WorldObjects
            if detect_collision(self, obj):
                if obj.solid == 100:  # Completely solid objects stops bullets
                    self.controller.ammo.remove(self)
                    try:
                        if obj.health:
                            obj.get_shot(self.damage)
                    except:
                        pass
                    return True  # if collision and cur ammo-object is removed, exit function



class NormalShot(Bullet):

    def __init__(self, player):

        speed = 10
        damage = 20
        width = 5
        height = 5
        sprite = pygame.image.load("images/ammo/basic_bullet.png")

        super(NormalShot, self).__init__(player, speed, damage, width, height, sprite)

        self.sprite.set_alpha(200) # apparency
        self.radius = 5
        self.name = "NormalShot"
        self.cooldown = 500

    def fire(self):
        """This is the function run when player presses the fire (1 or 2) button"""
        if self.cd_time == 0:
            self.player.controller.ammo.append(NormalShot(self.player))
            self.cd_time = self.cooldown






