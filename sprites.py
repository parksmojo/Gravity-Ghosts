import pygame

LIVE_COLOR = (255, 255, 255)

class Sprite(pygame.sprite.Sprite):
    def __init__(self, startx, starty, color):
        super().__init__()
        self.surf = pygame.Surface((40, 120))
        self.surf.fill(color)
        self.rect = self.surf.get_rect()
        self.rect.center = [startx, starty]

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.surf, self.rect)

class Player(Sprite):
    def __init__(self, startx, starty):
        super().__init__(startx, starty, LIVE_COLOR)
        self.speed = 5
        self.jumpspeed = 15
        self.vsp = 0
        self.gravity = 1
    
    def update(self, keys, floor):
        hsp = 0
        if self.rect.bottom > floor.top: onground = True
        else: onground = False
        # onground = pygame.Rect.colliderect(self.rect, floor)
        if keys[pygame.K_a]:
            hsp = -self.speed
        elif keys[pygame.K_d]:
            hsp = self.speed
        if keys[pygame.K_SPACE] and onground:
            self.vsp = -self.jumpspeed

        if self.vsp < 10 and not onground: self.vsp += self.gravity
        if self.vsp > 0 and onground: self.vsp = 0

        self.move(hsp,self.vsp)

    def move(self, x, y):
        self.rect.move_ip([x,y])

class Ghost(Sprite):
    def __init__(self, startx, starty):
        super().__init__(startx, starty)