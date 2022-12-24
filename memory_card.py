 Создай собственный Шутер!
from random import randint

from pygame import *
from time import time as timer

window = display.set_mode((1000, 700))
display.set_caption('Shooter')
background = transform.scale(image.load('fon4.jpg'), (1000, 700))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

clock = time.Clock()


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, width, height, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 605:
            self.rect.y += self.speed
        if keys[K_RIGHT] and self.rect.x < 935:
            self.rect.x += self.speed
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed

    def fire(self):
        bullet = Bullet('pulya-removebg-preview.png', self.rect.centerx - 6, self.rect.top, 15, 30, 20)
        bullets.add(bullet)


lost = 0
kills = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 700:
            self.rect.y = -40
            self.rect.x = randint(40, 660)
            lost += 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

font.init()
font1 = font.SysFont('Roboto', 40)
win = font1.render('Вы выиграли!', True, (255, 255, 255))
lose = font1.render('Вы проиграли!', True, (255, 255, 255))
ship = Player('gun.png', 45, 400, 80, 100, 10)
monsters = sprite.Group()
for i in range(5):
    monster = Enemy('zombi-removebg-preview.png', randint(40, 660), -40, 80, 40, randint(2,5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png', randint(40, 660), -40, 80, 40, randint(2, 5))
    asteroids.add(asteroid)
bullets = sprite.Group()
run = True
finish = False
life = 10
rel_time = False
num_fire = 0
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        keys = key.get_pressed()
        if keys[K_SPACE]:
            if num_fire < 50 and rel_time == False:
                ship.fire()
                num_fire += 1
        if num_fire >= 50 and rel_time == False:
            start = timer()
            rel_time = True
