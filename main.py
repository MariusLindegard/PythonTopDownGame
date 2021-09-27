import pygame, sys, random, time
from pygame.locals import *

ismainmenu = True
SCREEN_WIDTH = 1000
SCREEN_HEIGTH = 1000

pygame.init()
fps_clock = pygame.time.Clock()
screen = pygame.display.set_mode(([SCREEN_WIDTH, SCREEN_HEIGTH]))
# pygame.display.toggle_fullscreen()

def generate_noise(width, height):
    noise_map = []
    # Populate a noise map with 0s
    for y in range(height):
        new_row = []
        for x in range(width):
            new_row.append(0)
        noise_map.append(new_row)

    # Progressively apply variation to the noise map but changing values + or -
    # 5 from the previous entry in the same list, or the average of the
    # previous entry and the entry directly above
    new_value = 0
    top_of_range = 0
    bottom_of_range = 0
    for y in range(height):
        for x in range(width):
            if x == 0 and y == 0:
                continue
            if y == 0:  # If the current position is in the first row
                new_value = noise_map[y][x - 1] + random.randint(-1000, +1000)
            elif x == 0:  # If the current position is in the first column
                new_value = noise_map[y - 1][x] + random.randint(-1000, +1000)
            else:
                minimum = min(noise_map[y][x - 1], noise_map[y-1][x])
                maximum = max(noise_map[y][x - 1], noise_map[y-1][x])
                average_value = minimum + ((maximum-minimum)/2.0)
                new_value = average_value + random.randint(-1000, +1000)
            noise_map[y][x] = new_value
            # check whether value of current position is new top or bottom
            # of range
            if new_value < bottom_of_range:
                bottom_of_range = new_value
            elif new_value > top_of_range:
                top_of_range = new_value
    # Normalises the range, making minimum = 0 and maximum = 1
    difference = float(top_of_range - bottom_of_range)
    for y in range(height):
        for x in range(width):
            noise_map[y][x] = (noise_map[y][x] - bottom_of_range)/difference
    return noise_map

class World:
    def __init__(self):
        self.chunks = [
            [generate_noise(100, 100), generate_noise(100, 100), generate_noise(100, 100)],
            [generate_noise(100, 100), generate_noise(100, 100), generate_noise(100, 100)],
            [generate_noise(100, 100), generate_noise(100, 100), generate_noise(100, 100)],
            ]
            
        self.current_chunk = self.chunks[1][1]

world = World()
print(world.current_chunk)
    
class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH / 2 - 5
        self.y = SCREEN_HEIGTH / 2 - 5
        self.color = (255, 0, 255)
        self.movement_speed = 10
        self.health = 100
    
    def upgrade_movement_speed(self):
        if self.movement_speed < 10 and self.health > 50:
            self.movement_speed += 1

    def move_left(self):
        self.x -= self.movement_speed
        if self.x == 0:
            world.current_chunk = world.chunks[1][0]
            self.x = SCREEN_WIDTH - 50
    
    def move_right(self):
        self.x += self.movement_speed
        if self.x == SCREEN_WIDTH:
            world.current_chunk = world.chunks[1][2]
            self.x = 50

    def move_up(self):
        self.y -= self.movement_speed
        if self.y == 0:
            world.current_chunk = world.chunks[0][1]
            self.y = SCREEN_HEIGTH - 50
    
    def move_down(self):
        self.y += self.movement_speed
        if self.y == SCREEN_HEIGTH:
            world.current_chunk = world.chunks[2][1]
            self.y = 50


player_one = Player()

def key_pressed(key):
    keys = pygame.key.get_pressed()
    
    if keys[key]:
        return True


def update():
    pygame.display.update()


def draw():
    screen.fill((0, 0, 0))
    row = 0
    column = 0
    tile_size = 10



    for tile in world.current_chunk:
        for rows in tile:
            if rows > 0.7:
                pygame.draw.rect(screen, (165, 0, 78), (column - player_one.x, row - player_one.y, tile_size, tile_size))
            elif rows > 0.4:
                pygame.draw.rect(screen, (165, 255, 78), (column - player_one.x, row - player_one.y, tile_size, tile_size))
            else:
                pygame.draw.rect(screen, (0, 185, 10), (column - player_one.x, row - player_one.y, tile_size, tile_size))
                

            row += tile_size

        row = 0
        column += tile_size

    pygame.draw.rect(screen, player_one.color, (SCREEN_WIDTH / 2 - 5, SCREEN_HEIGTH / 2 - 5, 10, 10))
    label = pygame.font.SysFont('monospace', 15).render(f'Health: {player_one.health}', 1, (255, 0, 255))
    screen.blit(label, (pygame.display.get_surface().get_width()-100, 10))
    

def tick():
    if key_pressed(K_a):
        player_one.move_left()
    if key_pressed(K_d):
        player_one.move_right()
    if key_pressed(K_w):
        player_one.move_up()
    if key_pressed(K_s):
        player_one.move_down()
    if key_pressed(K_SPACE):
        world.map = generate_noise(100, 100)

    update()
    draw()
    
    
def mainmenu():
    label = pygame.font.SysFont('monospace', 15).render('Main Menu!', 1, (255, 255, 0))
    start = pygame.font.SysFont('monospace', 15).render('Press ENTER to start!', 1, (255, 255, 0))
    name = pygame.font.SysFont('monospace', 15).render('Fire and Water', 1, (255, 255, 0))

    screen.blit(name, (SCREEN_WIDTH / 2-70, 100))
    screen.blit(label, (SCREEN_WIDTH / 2-50, 200))
    screen.blit(start, (SCREEN_WIDTH / 2-100, 230))

    pygame.display.update()



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    
    while ismainmenu:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if pygame.K_KP_ENTER:
                    print('Enter pressed')
                    ismainmenu = False
        mainmenu()

    else:
        tick()
        fps_clock.tick(60)

