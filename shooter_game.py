from random import randint
from pygame import *
from time import time as timer

window = display.set_mode((700, 500))
display.set_caption("Shooter Game")
background = transform.scale(image.load('galaxy.jpg'), (700, 500))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, width, height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
# Игрок
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_d] and self.rect.x < 635:
            self.rect.x += self.speed
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed


    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 30, 15)
        bullets.add(bullet)
# Враг
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(30, 630)

            lost +=1

# Астеройд
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(30, 630)

asteroids = sprite.Group()
for i in range(3):
    aster = Asteroid('asteroid.png', randint(30,630), 0, 65, 65, randint(1,7))
    asteroids.add(aster)

# Пуля
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed

        if self.rect.y <= 0:
            self.kill()

lost = 0
score = 0

font.init()
font_lose = font.SysFont('Arial', 36)
font_win = font.SysFont('Arial', 36)

font_over = font.SysFont('Arial', 52)
win_text = font_over.render('YOU WIN', True, (255, 255, 255))
lose_text = font_over.render('YOU LOSE', True, (255, 255, 255))



player = Player('rocket.png', 300, 430, 65, 75, 5)
monsters = sprite.Group()
bullets = sprite.Group()


for i in range(5):
    enemy = Enemy('ufo.png', randint(30, 630), 0, 90, 50, randint(1,3))
    monsters.add(enemy)

mixer.init()
mixer.music.load('space.ogg')
fire_sound = mixer.Sound('fire.ogg')
mixer.music.play()

FPS = 60
clock = time.Clock()

finish = False
game = True

num_fire = 0
rel_time = False
while game:
    lost_score = font_lose.render('Пропущенно:' +str(lost), True, (255,255,255))
    win_score = font_lose.render('Счёт:' +str(score), True, (255,255,255))
    for e in event.get():
        if e.type == QUIT:
            game = False

        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    fire_sound.play()
                    player.fire()
                    num_fire += 1

                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    last_time = timer()

    if finish != True:
        window.blit(background, (0, 0))

        player.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        player.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        if rel_time:
            cur_time = timer()
            if cur_time - last_time <3:
                rel_rext = font.SysFont('Arial', 36). render('Wait, reload...', True, (200, 0 ,0))
                window.blit(rel_rext, (300, 465))
            else:
                num_fire = 0
                rel_time = False

        sprites_list = sprite.groupcollide(monsters, bullets, True, True)   
        for i in sprites_list:
            score +=1
            enemy = Enemy('ufo.png', randint(30, 630), 0, 90, 50, randint(1,3))
            monsters.add(enemy)

        if score >= 10:
            finish = True
            window.blit(win_text, (250, 250))   

        if lost >= 3 or sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False):

            finish = True
            window.blit(lose_text, (250, 250))

        window.blit(lost_score, (5, 70))
        window.blit(win_score, (5, 30))

    display.update()
    clock.tick(FPS)