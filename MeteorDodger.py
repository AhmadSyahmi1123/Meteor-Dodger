from turtle import title
import pygame, sys, random, time

class Spaceship(pygame.sprite.Sprite):
    def __init__(self,path,x_pos,y_pos):
        super().__init__()
        self.uncharged = pygame.image.load(path)
        self.charged = pygame.image.load('Assets\Meteor Dodger Assets\spaceship_charged.png')
        
        self.image = self.uncharged
        self.rect = self.image.get_rect(center = (x_pos,y_pos))
        self.shield_surface = pygame.image.load('Assets\Meteor Dodger Assets\shield.png')
        self.health = 5
        self.health_limit = 5
        self.damage = 1
        self.healed = 1
        
    def screen_constrain(self):
        if self.rect.right >= 1280:
            self.rect.right = 1280
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= 720:
            self.rect.bottom = 720

    def display_health(self):
        for index,shield in enumerate(range(self.health)):
            screen.blit(self.shield_surface,(10 + index * 40,10))

    def get_hit(self,damage):
        self.health -= self.damage

    def heal(self,healed):
        if self.health <= self.health_limit:
            self.health += self.healed
        if self.health >= self.health_limit:
            self.healed = 0

    def charge(self):
        self.image = self.charged

    def discharge(self):
        self.image = self.uncharged

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        self.screen_constrain()
        self.display_health()

class Meteor(pygame.sprite.Sprite):
    def __init__(self,path,x_pos,y_pos,x_speed, y_speed):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = (x_pos,y_pos))
        self.x_speed = x_speed
        self.y_speed = y_speed

    def update(self):
        self.rect.centerx += self.x_speed
        self.rect.centery += self.y_speed

        if self.rect.centery >= 750:
            self.kill()

class Shield(pygame.sprite.Sprite):
    def __init__(self,x_pos,y_pos,x_speed, y_speed):
        super().__init__()
        self.image = pygame.image.load('Assets\Meteor Dodger Assets\shield.png')
        self.rect = self.image.get_rect(center = (x_pos,y_pos))
        self.x_speed = x_speed
        self.y_speed = y_speed

    def update(self):
        self.rect.centerx += self.x_speed
        self.rect.centery += self.y_speed

        if self.rect.centery >= 750:
            self.kill()

class Laser(pygame.sprite.Sprite):
    def __init__(self,path,pos,speed):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed

    def update(self):
        self.rect.centery -= self.speed
        if self.rect.centery < -10:
            self.kill()

def main_game():
    global laser_active
    laser_group.draw(screen)
    laser_group.update()

    spaceship_group.draw(screen)
    spaceship_group.update()
    
    meteor_group.draw(screen)
    meteor_group.update()

    shield_group.draw(screen)
    shield_group.update()

    #Collision
    if pygame.sprite.spritecollide(spaceship_group.sprite,meteor_group,True):
        spaceship_group.sprite.get_hit(1)

    if pygame.sprite.spritecollide(spaceship_group.sprite,shield_group,True):
        spaceship_group.sprite.heal(1)

    for laser in laser_group:
        pygame.sprite.spritecollide(laser,meteor_group,True)

    if pygame.time.get_ticks() - laser_timer >= 500:
        laser_active = True
        spaceship_group.sprite.charge()

    return 1

def end_game():
    pygame.mouse.set_visible(True)
    game_over = game_over_font.render('Game Over',True,(255,255,255))
    game_over_rect = game_over.get_rect(center = (640,300))
    screen.blit(game_over,game_over_rect)

    score_text = score_font.render(f'Score: {score}',True,(255,255,255))
    score_rect = score_text.get_rect(center = (640,380))
    screen.blit(score_text,score_rect)

pygame.init()
screen_w = 1280
screen_h = 720
screen = pygame.display.set_mode((screen_w, screen_h))
clock = pygame.time.Clock()
pygame.display.set_caption('Meteor Dodger')
pygame.mouse.set_visible(False)

game_over_font = pygame.font.Font('Assets\Meteor Dodger Assets\LazenbyCompSmooth.ttf',100)
score_font = pygame.font.Font('Assets\Meteor Dodger Assets\LazenbyCompSmooth.ttf',30)
title_font = pygame.font.Font('Assets\Meteor Dodger Assets\LazenbyCompSmooth.ttf',100)
title = title_font.render('Meteor Dodger',True,(255,255,255))
title_rect = title.get_rect(center = (640,300))

score = 0
laser_timer = 0
laser_active = False

#Spaceship Sprite
spaceship = Spaceship('Assets\Meteor Dodger Assets\spaceship.png', 640, 360)
spaceship_group = pygame.sprite.GroupSingle()
spaceship_group.add(spaceship)

#Meteor Sprite
meteor_group = pygame.sprite.Group()

METEOR_EVENT = pygame.USEREVENT
pygame.time.set_timer(METEOR_EVENT, 200)

#Shield Sprite
shield_group = pygame.sprite.Group()

SHIELD_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SHIELD_EVENT, 2500)

#Laser Sprite
laser_group = pygame.sprite.Group()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
            
        if event.type == METEOR_EVENT:
            meteor_path = random.choice(['Assets\Meteor Dodger Assets\Meteor1.png','Assets\Meteor Dodger Assets\Meteor2.png','Assets\Meteor Dodger Assets\Meteor3.png'])
            random_x_pos = random.randrange(0,1280)
            random_y_pos = random.randrange(-500,-50)
            random_x_speed = random.randrange(-1,1)
            random_y_speed = random.randrange(4,10)
            meteor = Meteor(meteor_path,random_x_pos,random_y_pos,random_x_speed,random_y_speed)
            meteor_group.add(meteor)

        if event.type == SHIELD_EVENT:
            random_x_pos = random.randrange(0,1280)
            random_y_pos = random.randrange(-500,-50)
            random_x_speed = random.randrange(-1,1)
            random_y_speed = random.randrange(4,10)
            shield = Shield(random_x_pos,random_y_pos,random_x_speed,random_y_speed)
            shield_group.add(shield)
        
        if event.type == pygame.MOUSEBUTTONDOWN and laser_active:
            laser = Laser('Assets\Meteor Dodger Assets\Laser.png',event.pos,4)
            laser_group.add(laser)
            laser_active = False
            laser_timer = pygame.time.get_ticks()
            spaceship_group.sprite.discharge()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and spaceship_group.sprite.health <= 0:
                spaceship_group.sprite.health = 5
                meteor_group.empty()
                score = 0

    screen.fill((42,45,51))
    if spaceship_group.sprite.health >= 0:
        score += main_game()
    else:
        end_game()
            
            

    pygame.display.update()
    clock.tick(60)