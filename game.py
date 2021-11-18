import pygame
import os
import random

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800

IMG_PIPE = pygame.image.load(os.path.join('img','pipe.png'))
IMG_BG = pygame.image.load(os.path.join('img','bg.png'))
IMG_BASE = pygame.image.load(os.path.join('img','base.png'))
IMG_BIRD = [pygame.transform.scale2x(pygame.image.load(os.path.join('img','bird1.png'))),
            pygame.transform.scale2x(pygame.image.load(os.path.join('img','bird2.png'))),
            pygame.transform.scale2x(pygame.image.load(os.path.join('img','bird3.png')))
]

pygame.font.init()
SOURCE = pygame.font.SysFont('arial', 50)

class bird:
    IMGS = IMG_BIRD
    MAX_ROTATION = 25
    VELOCITY_ROTATION = 50
    TIME_ANIMATION = 5
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angule = 0
        self.velocity = 0
        self.height = self.y
        self.time = 0
        self.image_score = 0
        self.image = self.IMGS[0]
    
    def jump(self):
        self.velocity = -10.5
        self.time = 0
        self.height = self.y

    def move(self):
        self.time += 1
        displacement = 1.5 * (self.time**2) + self.velocity * self.time
        if displacement > 16:
            displacement = 16
        elif displacement < 0:
            displacement -= 2

        self.y += displacement
        if displacement < 0 or self.y < (self.height + 50):
            if self.angule > self.MAX_ROTATION:
                self.angule == self.MAX_ROTATION
            else:
                if self.angule > -90:
                    self.angule -= self.VELOCITY_ROTATION
        
    def draw(self, screen):
        self.image_score += 1
        if self.image_score < self.TIME_ANIMATION:
            self.image = self.IMGS[0]
        elif self.image_score < self.TIME_ANIMATION * 2:
            self.image = self.IMGS[1]
        elif self.image_score < self.TIME_ANIMATION * 3:
            self.image = self.IMGS[2]
        elif self.image_score < self.TIME_ANIMATION * 4:
            self.image = self.IMGS[1]
        elif self.image_score < self.TIME_ANIMATION * 4 + 1:
            self.image = self.IMGS[0]
            self.image_score = 0
        
        if self.angule < -80:
            self.image = self.IMGS[1]
            self.image_score = self.TIME_ANIMATION * 2

        img_rotate = pygame.transform.rotate(self.image, self.angule) 
        pos_center = self.image.get_rect(topleft=(self.x, self.y)).center
        rectangle = img_rotate.get_rect(center=pos_center)
        screen.blit(img_rotate, rectangle.topleft)

    def get_mask(self):
        pygame.mask.from_surface(self.image)


class pipe:
    distance = 200
    velocity_pipe = 5

    def __init__(self, x):
        self.x = x
        self.height = 0 
        self.pos_top = 0
        self.pos_base = 0 
        self.PIPE_TOP = pygame.transform.flip('IMG_PIPE', False, True)
        self.PIPE_BASE = IMG_PIPE
        self.spend = False
        self.define_height()

    def define_height(self):
        self.height = random.randrange(50, 450)
        self.pos_top = self.height - self.PIPE_TOP.get_height()
        self.pos_base = self.height - self.distance

    def move(self):
        self.x -= self.velocity_pipe

    def draw(self, screen):
        screen.blit(self.PIPE_TOP, (self.x, self.pos_top))
        screen.blit(self.PIPE_BASE, (self.x, self.pos_base))
    
    def collide(self):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        base_mask = pygame.mask.from_surface(self.PIPE_BASE)

        distance_top = (self.x - bird.x, self.pos_top - round(bird.y))
        distance_base = (self.x - bird.x, self.pos_base - round(bird.y))

        top_point = bird_mask.overlap(top_mask, distance_top)
        base_point = bird_mask.overlap(base_mask, distance_base)

        if base_point or top_point:
            return True
        else:
            return False


class base:
    velocity_base = 5
    width_base = IMG_BASE.get_width()
    IMG = IMG_BASE

    def __init__(self, y):
        self.y = y 
        self.x0 = 0
        self.x1 = self.width_base

    def move(self):
        self.x0 -= self.velocity_base
        self.x1 -= self.velocity_base
        if self.x0 + self.width_base < 0:
            self.x0 = self.x0 + self.width_base
        if self.x1 + self.width_base < 0:
            self.x1 = self.x1 + self.width_base

    def draw(self, screen):
        screen.blit(self.IMG, (self.x0, self.y))
        screen.blit(self.IMG, (self.x1, self.y))


def draw_screen(screen, birds, pipes, base, score):
    screen.blit(IMG_BG, (0,0))
    for bird in birds:
        bird.draw(screen)
    for pipe in pipes:
        pipe.draw(screen)

    text = SOURCE.render(f"PONTUAÇÂO: {score}", 1, (255,255,255))
    screen.blit(text, (SCREEN_WIDTH - 10 - text.get_width(), 10))
    base.draw(screen)
    pygame.display.update()

