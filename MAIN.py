import pygame
import random
import os

pygame.init()

# ================= MUSIC =================
pygame.mixer.init()

if os.path.exists("bg_music.mp3"):
    pygame.mixer.music.load("bg_music.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

# ================= SCREEN =================
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
clock = pygame.time.Clock()

# ================= COLORS =================
WHITE = (255,255,255)
RED = (255,80,80)
YELLOW = (255,255,0)
BLACK = (0,0,0)
GREEN = (40, 120, 40)
DIRT = (194, 178, 128)

# ================= ROAD =================
road_width = int(WIDTH * 0.6)
road_left = (WIDTH - road_width) // 2
lane_width = road_width // 3

LANES = [
    road_left + lane_width//2,
    road_left + lane_width + lane_width//2,
    road_left + 2*lane_width + lane_width//2
]

lane = 1

# ================= IMAGE LOAD =================
def load_image(path, size):
    if os.path.exists(path):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, size)
    else:
        surf = pygame.Surface(size)
        surf.fill(RED)
        return surf

car_img = load_image("car.png", (90,150))
enemy_img = load_image("enemy.png", (90,150))

# 🌳 TREE IMAGE (ADDED)
tree_img = load_image("tree.png", (100, 150))

# ================= TREES =================
trees = []

for i in range(30):
    side = random.choice(["left", "right"])

    if side == "left":
        x = random.randint(0, max(1, road_left - 50))
    else:
        x = random.randint(road_left + road_width + 20, WIDTH)

    y = random.randint(0, HEIGHT)
    trees.append([x, y])

# ================= GAME STATE =================
in_menu = True
game_over = False

player_y = HEIGHT - 180
enemies = []
speed = 5
score = 0

font_big = pygame.font.SysFont("Arial", 80)
font = pygame.font.SysFont("Arial", 50)

start_btn = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 80, 300, 80)
quit_btn = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 30, 300, 80)
restart_btn = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 80, 300, 100)

spawn_timer = 0
spawn_delay = 80

# ================= CONTROL =================
def set_lane(x):
    global lane
    if x < WIDTH/3:
        lane = 0
    elif x < WIDTH*2/3:
        lane = 1
    else:
        lane = 2

def reset():
    global enemies, score, speed, game_over, lane, spawn_timer
    enemies = []
    score = 0
    speed = 5
    lane = 1
    spawn_timer = 0
    game_over = False

def spawn():
    enemies.append([random.choice(LANES), -150])

# ================= BACKGROUND =================
def draw_background():
    screen.fill((120, 180, 255))

    pygame.draw.rect(screen, DIRT, (0, 0, road_left, HEIGHT))
    pygame.draw.rect(screen, DIRT, (road_left + road_width, 0, WIDTH, HEIGHT))

    pygame.draw.rect(screen, (25,25,25), (road_left, 0, road_width, HEIGHT))

    for i in range(0, HEIGHT, 60):
        pygame.draw.line(screen, WHITE,
                         (road_left+lane_width, i),
                         (road_left+lane_width, i+30), 3)
        pygame.draw.line(screen, WHITE,
                         (road_left+2*lane_width, i),
                         (road_left+2*lane_width, i+30), 3)

    # ================= TREES (IMAGE VERSION) =================
    for t in trees:
        x, y = t

        screen.blit(tree_img, (int(x), int(y)))

        t[1] += speed * 0.3

        if t[1] > HEIGHT:
            if x < road_left:
                t[0] = random.randint(0, max(1, road_left - 50))
            else:
                t[0] = random.randint(road_left + road_width + 20, WIDTH)
            t[1] = -120

# ================= MENU =================
def draw_menu():
    title = font_big.render("CAR RACING", True, WHITE)
    screen.blit(title, (WIDTH//2 - 220, HEIGHT//2 - 250))

    pygame.draw.rect(screen, GREEN, start_btn)
    pygame.draw.rect(screen, RED, quit_btn)

    screen.blit(font.render("START", True, BLACK), (start_btn.x+80, start_btn.y+15))
    screen.blit(font.render("QUIT", True, BLACK), (quit_btn.x+95, quit_btn.y+15))

# ================= LOOP =================
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if in_menu:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.collidepoint(event.pos):
                    in_menu = False
                if quit_btn.collidepoint(event.pos):
                    running = False
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    if restart_btn.collidepoint(event.pos):
                        reset()
                else:
                    set_lane(event.pos[0])

            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                set_lane(event.pos[0])

    if in_menu:
        draw_background()
        draw_menu()
        pygame.display.update()
        continue

    draw_background()

    if not game_over:
        score += 1

        if score % 500 == 0:
            speed += 0.5

        spawn_timer += 1
        if spawn_timer > spawn_delay:
            spawn()
            spawn_timer = 0

        for e in enemies:
            e[1] += speed

        enemies = [e for e in enemies if e[1] < HEIGHT]

        for e in enemies:
            if abs(e[0] - LANES[lane]) < 50 and e[1] > player_y - 100:
                game_over = True

    px = LANES[lane]
    screen.blit(car_img, (px-45, player_y))

    for e in enemies:
        screen.blit(enemy_img, (e[0]-45, e[1]))

    screen.blit(font.render(f"Score: {score}", True, YELLOW), (30,30))

    if game_over:
        over = font.render("GAME OVER", True, WHITE)
        screen.blit(over, (WIDTH//2-180, HEIGHT//2-100))

        pygame.draw.rect(screen, YELLOW, restart_btn)
        screen.blit(font.render("RESTART", True, BLACK),
                    (restart_btn.x+60, restart_btn.y+25))

    pygame.display.update()

pygame.quit()