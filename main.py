import pygame, asyncio, random, time
from pygame.locals import *
from pygame.sprite import Group

# Program constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60
BLACK = (0,0,0)
WHITE = (255,255,255)
DARK_GRAY = (75,75,75)
DARK_BLUE = (50,50,75)
GRAY = (128,128,128)
GREEN = (100,128,100)
YELLOW = (255,215,0)



# Classes
class Sprite(pygame.sprite.Sprite):
    def __init__(self, size, color, center, name = 'Sprite'):
        # Object set up
        super().__init__()
        self.width = size[0]
        self.height = size[1]
        self.surf = pygame.Surface((self.width, self.height))
        self.rect = self.surf.get_rect()
        self.surf.fill(color)
        self.rect.center = center
        self.name = name
        self.health = 1
        self.vsp = 0
        self.hsp = 0
        self.attack_time = 0
        self.facing = 1

    def draw(self, screen: pygame.Surface):
        screen.blit(self.surf, self.rect)

    def get_hit(self, damage, knock):
        self.health -= damage
        print(f"{self.name} Health: {self.health}")
        if self.health <= 0: self.kill()
        self.hsp = knock
        self.vsp = -abs(knock)

class Player(Sprite):
    def __init__(self, center):
        # Object set up
        size = (60,120)
        color = WHITE
        super().__init__(size, color, center, 'Player')

        # Background attributes
        self.prev_key = pygame.key.get_pressed()
        self.bullets: list[projectile] = []

        # Player attributes
        self.health = 100
        self.speed = 3
        self.sprint = 5
        self.jumpspeed = 15
        self.min_jumpspeed = 3
        self.gravity = 0.8
        self.drag = 1
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

        # Variable height jumping
        if self.prev_key[pygame.K_SPACE] and not keys[pygame.K_SPACE]:
            if self.vsp < -self.min_jumpspeed:
                self.vsp = -self.min_jumpspeed
        self.prev_key = keys

        # Gravity
        if self.vsp < 10 and not onground: self.vsp += self.gravity
        if self.vsp > 0 and onground: self.vsp = 0
        # Horizontal drag
        if self.hsp > 0 and not keys[pygame.K_d]: self.hsp -= self.drag
        elif self.hsp < 0 and not keys[pygame.K_a]: self.hsp += self.drag

        # Move the Character and the bullets
        self.rect.move_ip(self.hsp,self.vsp)
        for bullet in self.bullets:
            bullet.update()

    def check_collision(self, x, y, object):
        # Checks to see if will collide before colliding
        self.rect.move_ip([x,y])
        collide = pygame.rect.Rect.colliderect(self.rect, object)
        self.rect.move_ip([-x,-y])
        if collide and self.rect.bottom >= object.top:
            self.rect.bottom = object.top
        return collide

    def shoot(self):
        now = time.time()
        # Shoots a bullet if shot delay time has passed
        if now - self.attack_time > self.shot_delay:
            height = (self.rect.centery+self.rect.top)/2
            self.bullets.append(projectile((self.rect.centerx,height), self.facing))
            self.attack_time = now

    def draw(self, screen):
        for bullet in self.bullets:
            bullet.draw(screen)
        screen.blit(self.surf, self.rect)

class projectile():
    def __init__(self, center, facing):
        # Object set up
        self.x = center[0]
        self.y = center[1]
        self.radius = 6
        self.color = YELLOW
        self.facing = facing

        # Active attributes
        self.vel = 10
        self.damage = 20
        self.knock = 5

    def update(self):
        self.x += self.vel * self.facing

    def draw(self,screen):
        pygame.draw.circle(screen, self.color, (self.x,self.y), self.radius)

class Zombie(Sprite):
    def __init__(self, distance = 50, side = random.randrange(-1,2,2)):
        # Object set up
        size = (60,120)
        color = GREEN
        if side == 1: startx = SCREEN_WIDTH + distance # Defines on which side of screen the entity will spawn
        else: startx = -distance
        starty = floor.top - size[1] - 10
        super().__init__(size, color, (startx,starty), 'Zombie')

        # Active attributes
        self.health = 50
        self.speed = 1.2
        self.accel = 0.15
        self.gravity = 0.5
        self.drag = 1
        self.damage = 20
        self.knock = 10
        self.attack_delay = 0.5
        
    def update(self, floor):
        onground = self.rect.bottom >= floor.top
        now = time.time()

        # Will walk towards the player except after attacking
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

class Ghost(Sprite):
    def __init__(self, distance = 50, side = random.randrange(-1,2,2)):
        # Enemy set up
        size = (60,120)
        color = GRAY
        if side == 1: startx = SCREEN_WIDTH + distance # Defines on which side of screen the entity will spawn
        else: startx = -distance
        starty = 150
        super().__init__(size, color, (startx,starty), 'Ghost')

        # Active attributes
        self.health = 30
        self.speed = 2
        self.accel = 0.08
        self.drag = 1
        self.float_height = 20
        self.damage = 15
        self.knock = 10
        self.attack_delay = 0.5
        
    def update(self, floor):
        now = time.time()

        # Will float towards the player except after attacking
        if player.health > 0 and now - self.attack_time > self.attack_delay:
            if self.rect.right < player.rect.centerx:
                self.facing = 1
                if self.hsp < self.speed: self.hsp += self.speed * self.accel
            elif self.rect.left > player.rect.centerx:
                self.facing = -1
                if self.hsp > -self.speed: self.hsp += -self.speed * self.accel
        else: self.hsp = 0

        # Once on screen, floats down from start height to float height
        if self.rect.bottom < (floor.top - self.float_height) and self.rect.centerx < SCREEN_WIDTH and self.rect.centerx > 0: 
            self.rect.bottom += 0.8

        self.rect.move_ip(self.hsp, 0)

class Spider(Sprite):
    def __init__(self, distance = 50, side = random.randrange(-1,2,2)):
        # Enemy set up
        size = (90,50)
        color = BLACK
        if side == 1: startx = SCREEN_WIDTH + distance # Determines which side of screen the entity will spawn on
        else: startx = -distance
        starty = floor.top - size[1] - 10
        super().__init__(size, color, (startx,starty), 'Spider')
        self.facing = -side

        # Entity attributes
        self.health = 50
        self.speed = 2.5
        self.accel = 0.15
        self.gravity = 0.5
        self.drag = 1
        self.damage = 20
        self.knock = 10
        self.attack_delay = 0.5
        
    def update(self, floor):
        onground = self.rect.bottom >= floor.top
        now = time.time()

        # Walks in a constant direction across the screen until it leaves the screen
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



# Game initialization
pygame.init()
clock = pygame.time.Clock()

# Window initialization
pygame.display.set_caption('Ghosts')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.SCALED, vsync=1)

# Object making
floor = pygame.Rect(0, 450, SCREEN_WIDTH, SCREEN_HEIGHT - 400)
wall = pygame.Rect(75, 100, SCREEN_WIDTH - 150, SCREEN_HEIGHT-75)
player = Player((SCREEN_WIDTH/2, 400))
enemies = pygame.sprite.Group()
enemies.add(Zombie(0,1))
enemies.add(Zombie(0,-1))
enemies.add(Ghost(200,-1))
enemies.add(Ghost(200,1))
enemies.add(Spider(400,-1))
enemies.add(Spider(400,1))
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemies)

# Character creation, in a function to allow resetting
def reset():
    for enemy in enemies:
        enemy.kill()
    player.kill()
    player.__init__((SCREEN_WIDTH/2, 400))

    # Test wave
    spawned = []
    for i in range(0,5):
        type = random.randint(1,3)
        dist = i * 175
        match type:
            case 1:
                enemies.add(Zombie(dist))
                spawned.append('Zombie')
            case 2:
                enemies.add(Ghost(dist))
                spawned.append('Ghost')
            case 3:
                enemies.add(Spider(dist))
                spawned.append('Spider')
    print(spawned)
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
        screen.fill(BLACK)
        pygame.draw.rect(screen, (50,50,75), wall)
        for entity in all_sprites:
            entity.draw(screen)
        pygame.draw.rect(screen, (75,75,75), floor)

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)
asyncio.run(main())