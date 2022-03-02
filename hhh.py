import random
import pygame
import os
from os import path

# импорт папки игры
image_folders = path.join((__file__), 'Image')

width = 600  # Окно игры
height = 800
Black = (150, 255, 234)

FPS = 60
pygame.init()  # Запуск игры
pygame.mixer.init()  # Звук
pygame.font.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Игра Бога")
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):  # Игрок
    def __init__(self):  # Инициализация игрока
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((30, 30))  # Размер прямоуголника
        # self.image.fill((255, 145, 3))  # Цвет прямоуголника

        self.image = pygame.transform.scale(playerimg, (40, 50))  # прописываем переменную с картинкой и ее размер
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()  # Создание прямоуголника
        self.radius = 20
        # self.rect.center = (width / 2, height / 2)  # Центр прямоуголника
        self.rect.centerx = width / 2
        self.rect.bottom = height - 10
        self.speedx = 0

    def update(self):

        speeds = 6  # скорость для всех клавиш
        self.speedX = 0
        self.speedY = 0

        key_tracking = pygame.key.get_pressed()  # Словар совсеми клавишоми
        # можем добавить любые клавиши для передвижения игрока
        if key_tracking[pygame.K_LEFT]:
            self.speedX = -speeds

        if key_tracking[pygame.K_RIGHT]:
            self.speedX = speeds

        if key_tracking[pygame.K_a]:
            self.speedX = -speeds

        if key_tracking[pygame.K_d]:
            self.speedX = speeds

        if key_tracking[pygame.K_UP]:
            self.speedY = -speeds

        if key_tracking[pygame.K_DOWN]:
            self.speedY = speeds

        if key_tracking[pygame.K_w]:
            self.speedY = -speeds

        if key_tracking[pygame.K_s]:
            self.speedY = speeds

        self.rect.x += self.speedX
        self.rect.y += self.speedY

        # блок запрета движения
        if self.rect.right > width:
            self.rect.right = width

        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        a = Ammo(self.rect.centerx, self.rect.top)
        all_sprites.add(a)
        ammon.add(a)


class Enemy(pygame.sprite.Sprite):  # врага
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # self.image = pygame.Surface((50, 50))  # Размер врага (форма не определена)
        # self.image.fill((255, 54, 41))  # Цвет врага

        self.image_one = pygame.transform.scale(rockImg, (50, 60))  # прописываем переменную с картинкой и ее размер
        self.image_one.set_colorkey((255, 255, 255))

        self.image = self.image_one.copy()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()  # Создание врага по форме прямоугольника
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(4, 15)
        self.speedx = random.randrange(-3, 3)
        # проворт врага
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_one, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        if self.rect.top > height + 10 or self.rect.left < -25 or self.rect.right > width + 20:
            self.rect.x = random.randrange(width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Ammo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((5 , 10))
        # self.image.fill((255, 54, 41))
        self.image = pygame.transform.scale(buletImg, (30, 30))  # прописываем переменную с картинкой и ее размер
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -15

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:  # если выйдем за границу
            self.kill()  # убиваем процесс


# наша игровая графика загрузка картинок
backgrounds = pygame.image.load("Image/background.png").convert_alpha()
back_rect = backgrounds.get_rect()
playerimg = pygame.image.load("Image/player.png").convert_alpha()
buletImg = pygame.image.load("Image/Bulet.png").convert_alpha()
rockImg = pygame.image.load("Image/Rock2.png").convert_alpha()
# вариант создать новый список и пройтись в цикле по этому списку перебирая другие
# вариаты картинок например для врагов или пулек

all_sprites = pygame.sprite.Group()  # Добовление спрайта в групу
enemy = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
ammon = pygame.sprite.Group()

for i in range(4):  # спавним мобов кол-во
    mob = Enemy()
    all_sprites.add(mob)
    enemy.add(mob)

fontname = pygame.font.match_font('None')
score = 0


def scoretext(surf, text, size, x, y):
    colorss = (255, 255, 255)
    fontext = pygame.font.Font(fontname, size)
    # surf = pygame.font.render(text, True, colorss)
    txt = fontname.render(text, 1, colorss)
    recttext = txt.get_rect()
    recttext.midtop = (x, y)
    surf.blit(txt, recttext)


run = True
while run:

    clock.tick(FPS)  # Ограничения FPS

    for event in pygame.event.get():  # Выход на крестик
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # нажатие на пробел
                player.shoot()  # вызов функции стрельбы

    all_sprites.update()

    collision = pygame.sprite.groupcollide(enemy, ammon, True, True)  # столкновение пули и врага
    for i in collision:
        mob = Enemy()
        all_sprites.add(mob)
        enemy.add(mob)
        score = score + 1
        print(score)

    collision = pygame.sprite.spritecollide(player, enemy, False)  # столкновение пули и игрока
    if collision:
        run = False

    screen.fill(Black)  # Заливка основного цвета
    screen.blit(backgrounds, back_rect)
    all_sprites.draw(screen)
    scoretext(screen, 'fff', 8, width / 2, 10)

    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
