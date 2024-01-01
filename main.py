import pygame, asyncio, random, time
from pygame.locals import *
from pygame.sprite import Group

# Program constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60
BACKGROUND = (0, 0, 0)
LIVE_COLOR = (255, 255, 255)

# Classes
class Sprite(pygame.sprite.Sprite):
    def __init__(self, width, height, color, center, name = 'Sprite'):
        super().__init__()
        self.width = width
        self.height = height
        self.surf = pygame.Surface((self.width, self.height))
        self.rect = self.surf.get_rect()
        self.surf.fill(color)
        self.rect.center = center
        self.name = name

    def draw(self, screen: pygame.Surface):
        screen.blit(self.surf, self.rect)

    def get_hit(self, damage, knock):
        self.health -= damage
        print(f"{self.name} Health: {self.health}")
        if self.health <= 0: self.kill()
        self.hsp = knock
        self.vsp = -abs(knock)

class Player(pygame.sprite.Sprite):
    def __init__(self, startx, starty):
        super().__init__()
        # Player set up
        self.width = 60
        self.height = 120
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill(LIVE_COLOR)
        self.rect = self.surf.get_rect()
        self.rect.center = [startx, starty]
        self.prev_key = pygame.key.get_pressed()

        # Player attributes
        self.health = 100
        self.speed = 3
        self.sprint = 5
        self.jumpspeed = 15
        self.min_jumpspeed = 3
        self.gravity = 0.8
        self.vsp = 0
        self.drag = 1
        self.hsp = 0
        self.facing = 1
        self.bullets: list[projectile] = []
        self.shot_time = 0
        self.shot_delay = 0.6
    
    def update(self, keys, floor):
        onground = self.check_collision(0,1,floor)

        # User Control
        if self.health > 0:
            if keys[pygame.K_a]:
                self.facing = -1
                if keys[pygame.K_LSHIFT]: self.hsp = -self.sprint
                else: self.hsp = -self.speed
            elif keys[pygame.K_d]:
                self.facing = 1
                if keys[pygame.K_LSHIFT]: self.hsp = self.sprint
                else: self.hsp = self.speed
            if keys[pygame.K_SPACE] and onground:
                self.vsp = -self.jumpspeed
            if keys[pygame.K_k]:
                self.shoot()
            if keys[pygame.K_LCTRL]:
                self.rect.height = self.height / 2
            elif self.prev_key[pygame.K_LCTRL] and not keys[pygame.K_LCTRL]:
                self.rect.height = self.height

        # Location correction
        if self.rect.left < 0: self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH: self.rect.right = SCREEN_WIDTH

        # variable height jumping
        if self.prev_key[pygame.K_SPACE] and not keys[pygame.K_SPACE]:
            if self.vsp < -self.min_jumpspeed:
                self.vsp = -self.min_jumpspeed
        self.prev_key = keys

        # Gravity
        if self.vsp < 10 and not onground: self.vsp += self.gravity
        if self.vsp > 0 and onground: self.vsp = 0
        # Drag
        if self.hsp > 0 and not keys[pygame.K_d]: self.hsp -= self.drag
        elif self.hsp < 0 and not keys[pygame.K_a]: self.hsp += self.drag

        self.move(self.hsp,self.vsp)
        for bullet in self.bullets:
            bullet.update()

    def check_collision(self, x, y, object):
        self.rect.move_ip([x,y])
        collide = pygame.rect.Rect.colliderect(self.rect, object)
        self.rect.move_ip([-x,-y])
        if collide and self.rect.bottom >= object.top:
            self.rect.bottom = object.top
            # self.vsp = 0
        return collide

    def move(self, x, y):
        self.rect.move_ip([x,y])

    def shoot(self):
        now = time.time()
        if now - self.shot_time > self.shot_delay:
            height = (self.rect.centery+self.rect.top)/2
            new_bullet = projectile(self.rect.centerx,height, self.facing)
            self.bullets.append(new_bullet)
            self.shot_time = now

    def get_hit(self, damage, knock):
        self.health -= damage
        print(f"Player Health: {self.health}, get_hit with knock: {knock}")
        if self.health <= 0: self.kill()
        self.hsp = knock
        self.vsp = -abs(knock)

    def draw(self, screen):
        for bullet in self.bullets:
            bullet.draw(screen)
        screen.blit(self.surf, self.rect)

class projectile():
    def __init__(self, x, y, facing):
        self.x = x
        self.y = y
        self.radius = 6
        self.color = (255,215,0)
        self.facing = facing
        self.vel = facing * 10
        self.damage = 20
        self.knock = 5

    def update(self):
        self.x += self.vel

    def draw(self,screen):
        pygame.draw.circle(screen, self.color, (self.x,self.y), self.radius)

class Zombie(pygame.sprite.Sprite):
    def __init__(self, distance = 50):
        super().__init__()
        # Enemy set up
        self.surf = pygame.Surface((60, 120))
        self.surf.fill((100,128,100))
        self.rect = self.surf.get_rect()
        starty = floor.top - 10
        if random.randint(1,2) == 1: startx = -distance
        else: startx = SCREEN_WIDTH + distance
        self.rect.bottomleft = [startx, starty]

        # Enemy attributes
        self.health = 50
        self.speed = 1.2
        self.accel = 0.15
        self.facing = 1
        self.gravity = 0.5
        self.vsp = 0
        self.drag = 1
        self.hsp = 0
        self.damage = 20
        self.knock = 10
        self.attack_time = 0
        self.attack_delay = 0.5

    def get_hit(self, damage, knock):
        self.health -= damage
        print(f"Zombie Health: {self.health}")
        if self.health <= 0: self.kill()
        self.hsp = knock
        self.vsp = -abs(knock)
        
    def update(self, floor):
        onground = self.rect.bottom >= floor.top
        now = time.time()

        if player.health > 0 and now - self.attack_time > self.attack_delay:
            if self.rect.right < player.rect.centerx:
                self.facing = 1
                if self.hsp < self.speed: self.hsp += self.speed * self.accel
            elif self.rect.left > player.rect.centerx:
                self.facing = -1
                if self.hsp > -self.speed: self.hsp += -self.speed * self.accel
        else: self.hsp = 0
        
        # Gravity
        if self.vsp < 10 and not onground: self.vsp += self.gravity
        if self.vsp > 0 and onground: self.vsp = 0

        self.rect.move_ip(self.hsp, self.vsp)

    def draw(self, screen):
        screen.blit(self.surf, self.rect)

class Ghost(pygame.sprite.Sprite):
    def __init__(self, distance = 50):
        super().__init__()
        # Enemy set up
        self.surf = pygame.Surface((60, 120))
        self.surf.fill((128,128,128))
        self.rect = self.surf.get_rect()
        starty = 150
        if random.randint(1,2) == 1: startx = -distance
        else: startx = SCREEN_WIDTH + distance
        self.rect.bottomleft = [startx, starty]

        # Enemy attributes
        self.health = 30
        self.speed = 2
        self.accel = 0.08
        self.facing = 1
        self.drag = 1
        self.hsp = 0
        self.damage = 15
        self.knock = 10
        self.attack_time = 0
        self.attack_delay = 0.5

    def get_hit(self, damage, knock):
        self.health -= damage
        print(f"Ghost Health: {self.health}")
        if self.health <= 0: self.kill()
        self.hsp = knock
        
    def update(self, floor):
        now = time.time()

        if player.health > 0 and now - self.attack_time > self.attack_delay:
            if self.rect.right < player.rect.centerx:
                self.facing = 1
                if self.hsp < self.speed: self.hsp += self.speed * self.accel
            elif self.rect.left > player.rect.centerx:
                self.facing = -1
                if self.hsp > -self.speed: self.hsp += -self.speed * self.accel
        else: self.hsp = 0

        if self.rect.bottom < floor.top - 15 and self.rect.centerx < SCREEN_WIDTH and self.rect.centerx > 0: 
            self.rect.bottom += 0.8
        self.rect.move_ip(self.hsp, 0)

    def draw(self, screen):
        screen.blit(self.surf, self.rect)

class Spider(pygame.sprite.Sprite):
    def __init__(self, distance = 50):
        super().__init__()
        # Enemy set up
        self.surf = pygame.Surface((90, 50))
        self.surf.fill((0,0,0))
        self.rect = self.surf.get_rect()
        starty = floor.top - 10
        if random.randint(1,2) == 1:
            startx = -distance # Spawn Left Side
            self.facing = 1
        else:
            startx = SCREEN_WIDTH + distance # Spawn Right Side
            self.facing = -1
        self.rect.bottomleft = [startx, starty]

        # Enemy attributes
        self.health = 50
        self.speed = 2.5
        self.accel = 0.15
        self.gravity = 0.5
        self.vsp = 0
        self.drag = 1
        self.hsp = 0
        self.damage = 20
        self.knock = 10
        self.attack_time = 0
        self.attack_delay = 0.5

    def get_hit(self, damage, knock):
        self.health -= damage
        print(f"Spider Health: {self.health}")
        if self.health <= 0: self.kill()
        self.hsp = knock
        self.vsp = -abs(knock)
        
    def update(self, floor):
        onground = self.rect.bottom >= floor.top
        now = time.time()

        if player.health > 0:
            if self.facing == 1:
                if self.hsp < self.speed: self.hsp += self.speed * self.accel
                if self.rect.centerx > SCREEN_WIDTH + 100: self.kill()
            elif self.facing == -1:
                if self.hsp > -self.speed: self.hsp += -self.speed * self.accel
                if self.rect.centerx < -100: self.kill()
        else: self.hsp = 0
        
        # Gravity
        if self.vsp < 10 and not onground: self.vsp += self.gravity
        if self.vsp > 0 and onground: self.vsp = 0

        self.rect.move_ip(self.hsp, self.vsp)

    def draw(self, screen):
        screen.blit(self.surf, self.rect)

# Game initialization
pygame.init()
clock = pygame.time.Clock()

# Window initialization
pygame.display.set_caption('Ghosts')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.SCALED, vsync=1)

# Object making
floor = pygame.Rect(0, 450, SCREEN_WIDTH, SCREEN_HEIGHT - 400)
wall = pygame.Rect(75, 100, SCREEN_WIDTH - 150, SCREEN_HEIGHT-75)
player = Player(SCREEN_WIDTH/2, 400)
enemies = pygame.sprite.Group()
enemies.add(Zombie())
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemies)

# Character creation, in a function to allow resetting
def reset():
    for enemy in enemies:
        enemy.kill()
    player.kill()
    player.__init__(SCREEN_WIDTH/2, 400)

    # Test wave
    for i in range(0,4):
        type = random.randint(1,3)
        dist = i * 175
        match type:
            case 1:
                enemies.add(Zombie(dist))
            case 2:
                enemies.add(Ghost(dist))
            case 3:
                enemies.add(Spider(dist))
    all_sprites.add(player)
    all_sprites.add(enemies)

# Game loop
async def main():
    round_done = False
    running = True
    while running:
        # Dealing with events
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_r:
                    reset()
                    round_done = False
                elif event.key == K_p:
                    print(f'Enemies left: {len(enemies.sprites())}')
            elif event.type == QUIT:
                running = False

        # Collision checks
        for enemy in enemies:
            for bullet in player.bullets:
                if enemy.rect.collidepoint(bullet.x,bullet.y):
                    enemy.get_hit(bullet.damage, bullet.facing * bullet.knock)
                    player.bullets.pop(player.bullets.index(bullet))
                    # print(f"Enemies left: {len(enemies.sprites())}")

            if player.rect.colliderect(enemy.rect):
                if player.health > 0:
                    now = time.time()
                    if now - enemy.attack_time > enemy.attack_delay:
                        player.get_hit(enemy.damage, enemy.facing * enemy.knock)
                        enemy.attack_time = now
            
        if len(enemies.sprites()) == 0 and not round_done:
            print("Round Won!")
            round_done = True

        # Update
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys, floor)
        for enemy in enemies:
            enemy.update(floor)

        # Draw the frame
        screen.fill(BACKGROUND)
        pygame.draw.rect(screen, (50,50,75), wall)
        for entity in all_sprites:
            entity.draw(screen)
        pygame.draw.rect(screen, (75,75,75), floor)

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)
asyncio.run(main())