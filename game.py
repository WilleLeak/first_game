import pygame
from random import randint, choice


# importing for easier access to key coords
from pygame.locals import (
    K_w,
    K_a,
    K_s,
    K_d,
    K_SPACE,
    K_ESCAPE,
    KEYUP,
    KEYDOWN,
    QUIT
)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load(file_loc + "graphics/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load(file_loc + "graphics/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = player_walk_1 = pygame.image.load(file_loc + "graphics/jump.png").convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 420))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[K_SPACE] and self.rect.bottom >= 420:
            self.gravity = -21

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 420:
            self.rect.bottom = 420

    def animation_state(self):
        if self.rect.bottom < 420:
            self.image = self.player_jump
        else: 
            self.player_index += .1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]


    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == "fly":
            fly_1 = pygame.image.load(file_loc + "graphics/fly1.png").convert_alpha()
            fly_2 = pygame.image.load(file_loc + "graphics/fly2.png").convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 300
        else:
            snail_1 = pygame.image.load(file_loc + "graphics/snail1.png").convert_alpha()
            snail_2 = pygame.image.load(file_loc + "graphics/snail2.png").convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 420

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += .1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]


    def update(self):
        self.animation_state()
        self.rect.x -= 5
        self.destroy()

    def destroy(self):
        if self.rect.right <= -10:
            self.kill()


# functions
def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score_su = font.render(f"Score: {current_time // 1000}", False, "Black")
    score_rect = score_su.get_rect(center = (SCREEN_WIDTH / 2, 30))
    screen.blit(score_su, score_rect)
    return current_time // 1000

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


# constants for file input
file_loc = "python practice/python stuff/first game/"

# vars
game_active = False
start_time = 0
score = 0

# initialize pygame
pygame.init()

# constants for screen size
SCREEN_WIDTH = 549
SCREEN_HEIGHT = 478

# screen object created
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("counter strike")


# clock to keep track of game time
clock = pygame.time.Clock()

# font type
font = pygame.font.Font(file_loc + "font/PixelType.ttf", 50)

background_su = pygame.image.load(file_loc + "graphics/city background.jpg").convert()
ground_su = pygame.image.load(file_loc + "graphics/roof.png").convert()

# groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()


# intro screen
player_stand = pygame.image.load(file_loc + "graphics/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 3)
player_stand_rect = player_stand.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

game_name = font.render("counter strike", False, "Black")
game_name_rect = game_name.get_rect(center = (SCREEN_WIDTH / 2, 50))

start_ins = font.render("press space to start", False, "Black")
start_ins_rect = start_ins.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50))

# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1000)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

# main game loop
while True:
    # looking at every event in queue
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        if game_active:
             if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(["fly", "snail", "snail", "snail"])))
        else:
            if event.type == KEYDOWN and event.key == K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()

          

    if game_active:
        screen.blit(background_su, (0, 0))
        screen.blit(ground_su, (0, 420))
        score = display_score()


        # main player character
        player.draw(screen)
        player.update()

        # obstacle movement
        obstacle_group.draw(screen)
        obstacle_group.update()

        # collison
        game_active = collision_sprite()


    else:
        screen.fill("Grey")
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_name, game_name_rect)

        # empty enemy list

        score_msg = font.render(f"Score: {score}", False, "Black")
        score_msg_rect = score_msg.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50))
        if score == 0:
            screen.blit(start_ins, start_ins_rect)
        else: 
            screen.blit(score_msg, score_msg_rect)


    pygame.display.update()
    clock.tick(60)