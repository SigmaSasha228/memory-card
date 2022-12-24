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
           
    if not finish:
        window.blit(background, (0, 0))
        ship.reset()
        ship.update()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        asteroids.draw(window)
        asteroids.update()
        text_lost = font1.render('Пропущено:' + str(lost), True, (255, 255, 255))
        text_kills = font1.render('Сбитых:' + str(kills), True, (255, 255, 255))
        text_life = font1.render('Жизни:' + str(life), True, (255, 255, 255))
        window.blit(text_lost, (10, 60))
        window.blit(text_kills, (10, 20))
        window.blit(text_life, (10, 100))
        if rel_time == True:
            new = timer()
            if new - start < 3:
                reload = font1.render('Перезарядка....', True, (255, 255, 255))
                window.blit(reload, (400, 350))
            else:
                rel_time = False
                num_fire = 0
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            kills += 1
            monster = Enemy('zombi-removebg-preview.png', randint(40, 660), -40, 80, 40, randint(2,5))
            monsters.add(monster)
        if sprite.spritecollide(ship, monsters, False)  or sprite.spritecollide(ship, asteroids, False):
            life -= 1
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
        if life == 0 or lost >= 10:
            finish = True
            window.blit(lose, (400, 350))
        if kills >= 10:
            finish = True
            window.blit(win, (400, 350))
    else:
        finish = False
        kills = 0
        lost = 0
        time.delay(3000)

        for m in monsters:
            m.kill()
        for b in bullets:
            b.kill()
