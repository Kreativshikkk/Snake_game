import pygame
import random

WIDTH = 1152
HEIGHT = 720
x, y = WIDTH / 2, HEIGHT / 2
FPS = 100
length = 30
y += length

# music
pygame.mixer.init()
pygame.mixer.music.load("Pixies_-_Where_Is_My_Mind_(ColdMP3.com).mp3")
pygame.mixer.music.play(-1)

# Coords_list
coords = []
# Setting colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
# Making a game and a window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fight snake")
clock = pygame.time.Clock()
# Making images for snake and buffs
player_img = pygame.image.load("Tylerbetterpicture.png").convert()
player_img = pygame.transform.scale(player_img, (length, length))
buff_img = pygame.image.load("edward_norton.png").convert()
buff_img = pygame.transform.scale(buff_img, (50, 50))
wall_img = pygame.image.load("wall.png").convert()
wall_img = pygame.transform.scale(wall_img, (WIDTH, HEIGHT))


# Objects
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self, x, y):
        self.rect.center = (x, y)


class Buff(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = buff_img
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(50, 670), random.randint(50, 670))

    def get_coords(self):
        try:
            return self.rect.center
        except AttributeError:
            return (5 * WIDTH, 5 * HEIGHT)


class New_player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()

    def update(self, num, coords):
        self.rect.center = coords[-1 - length * num]


snake = {}

# spirit preparation
all_sprites = pygame.sprite.Group()
player = Player()
buff = Buff()
all_sprites.add(buff)
snake = {0: player}
# making a number for next snake spirits
a = 0
# making a game_over marker
b = 0
# Game cycle
running = True
status = 'up'  # moving up as default
while running:
    pressed = pygame.key.get_pressed()
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT or pressed[pygame.K_ESCAPE]:
            running = False
    # Keep the cycle on the right speed
    clock.tick(FPS)

    # color_setting
    color = (0, 228, 228)
    screen.fill(color)
    screen.blit(wall_img, (0, 0))
    # mechanics

    # statuses
    if pressed[pygame.K_UP] and status != 'down' and b != 1:
        status = 'up'
    if pressed[pygame.K_DOWN] and status != 'up' and b != 1:
        status = 'down'
    if pressed[pygame.K_LEFT] and status != 'left' and b != 1:
        status = 'right'
    if pressed[pygame.K_RIGHT] and status != 'right' and b != 1:
        status = 'left'
    if pressed[pygame.K_w] and pressed[pygame.K_a] and status != 'down_right' and b != 1:
        status = 'up_left'
    if pressed[pygame.K_s] and pressed[pygame.K_a] and status != 'up_right' and b != 1:
        status = 'down_left'
    if pressed[pygame.K_s] and pressed[pygame.K_d] and status != 'up_left' and b != 1:
        status = 'down_right'
    if pressed[pygame.K_w] and pressed[pygame.K_d] and status != 'down_left' and b != 1:
        status = 'up_right'
    # moving
    if status == 'down':
        y += 1
    if status == 'up':
        y -= 1
    if status == 'left':
        x += 1
    if status == 'right':
        x -= 1
    if status == 'up_left':
        y -= 1
        x -= 1
    if status == 'up_right':
        y -= 1
        x += 1
    if status == 'down_left':
        y += 1
        x -= 1
    if status == 'down_right':
        y += 1
        x += 1
    if y > HEIGHT:
        y -= HEIGHT
    if x > WIDTH:
        x -= WIDTH
    if y < 0:
        y += HEIGHT
    if x < 0:
        x += WIDTH
    # updating coords, checking for death
    coords.append((x, y))
    forbidden_status = ['up_left', 'up_right', 'down_left', 'down_right']
    for i in range(1, a + 1):
        if abs(x - coords[-1 - i * length][0]) < length / 2 and abs(
                y - coords[-1 - i * length][1]) < length / 2 and a > 0 and status not in forbidden_status:
            status = ''
            font = pygame.font.SysFont("Arial", 72)
            txtsurf = font.render(f"Game over, bro. Your score is {a}", True, (255, 250, 205))
            screen.blit(txtsurf, ((WIDTH - txtsurf.get_width()) // 2, (HEIGHT - txtsurf.get_height()) // 2))
            if b == 0:
                b = 1
                time_0 = pygame.time.get_ticks()
                pygame.mixer.music.pause()
                pygame.mixer.music.load(
                    "I'm not Tyler Durden! I'm Tyler Durden.mp3")
                pygame.mixer.music.play(1)
            if pygame.time.get_ticks() >= time_0 + 9500:
                running = False

    # increasing size
    if abs(coords[-1][0] - Buff.get_coords(buff)[0]) <= 20 and abs(coords[-1][1] - Buff.get_coords(buff)[1]) <= 20:
        a += 1
        snake[a] = New_player()
        all_sprites.add(snake[a])
        buff_new = Buff()
        all_sprites.remove(buff)
        buff = None
        all_sprites.add(buff_new)
        buff = buff_new
    #score output
    font = pygame.font.SysFont("Arial", 25)
    txtsurf = font.render(f"Score: {a}", True, (255, 250, 205))
    screen.blit(txtsurf, ((0, 0)))
    all_sprites.add(player)
    all_sprites.add(buff)
    player.update(x, y)
    for i in snake:
        all_sprites.add(snake[i])
        if i != 0:
            New_player.update(snake[i], i, coords)
    all_sprites.draw(screen)
    pygame.display.flip()
    pygame.display.update()

pygame.quit()
