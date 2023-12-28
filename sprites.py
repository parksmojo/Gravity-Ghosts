import pygame

LIVE_COLOR = (255, 255, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self, startx, starty):
        super().__init__()
        # Player set up
        self.surf = pygame.Surface((40, 120))
        self.surf.fill(LIVE_COLOR)
        self.rect = self.surf.get_rect()
        self.rect.center = [startx, starty]

        # Player values
        self.speed = 5
        self.jumpspeed = 15
        self.vsp = 0
        self.gravity = 0.8
        self.min_jumpspeed = 3
        self.prev_key = pygame.key.get_pressed()
    
    def update(self, keys, floor):
        hsp = 0
        onground = self.check_collision(0,1,floor)

        # User Control
        if keys[pygame.K_a]:
            if self.rect.left > 0:
                hsp = -self.speed
        elif keys[pygame.K_d]:
            if self.rect.right < 1000:
                hsp = self.speed
        if keys[pygame.K_SPACE] and onground:
            self.vsp = -self.jumpspeed

        # variable height jumping
        if self.prev_key[pygame.K_SPACE] and not keys[pygame.K_SPACE]:
            if self.vsp < -self.min_jumpspeed:
                self.vsp = -self.min_jumpspeed
        self.prev_key = keys

        # Gravity
        if self.vsp < 10 and not onground: self.vsp += self.gravity
        if self.vsp > 0 and onground: self.vsp = 0

        self.move(hsp,self.vsp)

    def check_collision(self, x, y, object):
        self.rect.move_ip([x,y])
        collide = pygame.rect.Rect.colliderect(self.rect, object)
        self.rect.move_ip([-x,-y])
        if collide and self.rect.bottom >= object.top:
            self.rect.bottom = object.top
            self.vsp = 0
        return collide

    def move(self, x, y):
        self.rect.move_ip([x,y])

    def draw(self, screen):
        screen.blit(self.surf, self.rect)

class Ghost(pygame.sprite.Sprite):
    def __init__(self, startx, starty):
        super().__init__()