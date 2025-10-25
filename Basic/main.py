"""Simple Alien Shooter made with PyGame Zero.

Controls:
 - Left / Right arrows to move
 - Space to shoot
 - R to restart after game over

Run with:
  pgzrun main.py
or
  python -m pgzero main.py

This implementation uses simple shapes so no external image assets are required.
"""

import random
import time
import math
import pygame

# --- Window
WIDTH = 480
HEIGHT = 640
TITLE = "Alien Shooter - PyGame Zero"

# --- Player
player = {
    "x": WIDTH // 2,
    "y": HEIGHT - 48,
    "w": 48,
    "h": 18,
    "speed": 300,
}

# --- Bullets
bullets = []  # each bullet: {x, y, vy}
SHOT_COOLDOWN = 0.25
last_shot = 0.0

# --- Aliens
aliens = []  # each alien: {x, y, vx, vy, size}
ALIEN_SPAWN_INTERVAL = 1.0
last_spawn = 0.0
alien_direction = 1

# --- Game state
score = 0
lives = 3
game_over = False

MAX_ALIENS = 8


def spawn_alien():
    """Create a new alien at top with random x and speed."""
    size = random.randint(18, 30)
    x = random.randint(size, WIDTH - size)
    y = -size
    vx = random.choice([-1, 1]) * random.uniform(20, 80)
    vy = random.uniform(10, 40)
    aliens.append({"x": x, "y": y, "vx": vx, "vy": vy, "size": size})


def restart():
    global bullets, aliens, score, lives, game_over, last_spawn, last_shot
    bullets = []
    aliens = []
    score = 0
    lives = 3
    game_over = False
    last_spawn = time.time()
    last_shot = 0.0


def update(dt):
    global last_shot, last_spawn, score, lives, game_over
    if game_over:
        return

    # Player movement
    if keyboard.left:
        player["x"] -= player["speed"] * dt
    if keyboard.right:
        player["x"] += player["speed"] * dt
    # clamp
    half_w = player["w"] / 2
    if player["x"] < half_w:
        player["x"] = half_w
    if player["x"] > WIDTH - half_w:
        player["x"] = WIDTH - half_w

    # Shooting (cooldown)
    now = time.time()
    if keyboard.space and now - last_shot > SHOT_COOLDOWN:
        shoot()
        last_shot = now

    # Update bullets
    for b in bullets[:]:
        b["y"] += b["vy"] * dt
        if b["y"] < -10:
            bullets.remove(b)

    # Update aliens
    for a in aliens[:]:
        a["x"] += a["vx"] * dt
        a["y"] += a["vy"] * dt

        # bounce on sides
        if a["x"] - a["size"] < 0:
            a["x"] = a["size"]
            a["vx"] *= -1
            a["y"] += 8
        if a["x"] + a["size"] > WIDTH:
            a["x"] = WIDTH - a["size"]
            a["vx"] *= -1
            a["y"] += 8

        # collision with player
        if collide_circle_rect(a["x"], a["y"], a["size"], player_rect()):
            aliens.remove(a)
            lives -= 1
            if lives <= 0:
                game_over = True

    # Bullet-alien collisions
    for b in bullets[:]:
        for a in aliens[:]:
            if collide_circle_point(a["x"], a["y"], a["size"], b["x"], b["y"]):
                try:
                    bullets.remove(b)
                except ValueError:
                    pass
                try:
                    aliens.remove(a)
                except ValueError:
                    pass
                score += 10
                break

    # Spawn aliens over time up to limit
    if now - last_spawn > ALIEN_SPAWN_INTERVAL and len(aliens) < MAX_ALIENS:
        spawn_alien()
        last_spawn = now


def draw():
    screen.clear()
    # background
    screen.fill((8, 12, 30))

    # draw player as a triangle
    px = player["x"]
    py = player["y"]
    w = player["w"]
    h = player["h"]
    points = [(px - w // 2, py + h // 2), (px + w // 2, py + h // 2), (px, py - h // 2)]
    # Draw filled triangle
    pygame.draw.polygon(screen.surface, (100, 200, 255), points)
    # Draw outline
    pygame.draw.polygon(screen.surface, (200, 255, 255), points, 1)

    # bullets
    for b in bullets:
        pygame.draw.rect(screen.surface, (255, 240, 100), 
                        pygame.Rect(b["x"] - 2, b["y"] - 6, 4, 12))

    # aliens
    for a in aliens:
        pygame.draw.circle(screen.surface, (180, 80, 160), 
                         (int(a["x"]), int(a["y"])), a["size"])
        pygame.draw.circle(screen.surface, (230, 140, 210), 
                         (int(a["x"]), int(a["y"])), a["size"], 1)

    # HUD
    screen.draw.text("Score: " + str(score), (8, 8), fontsize=28, color=(220, 220, 220))
    screen.draw.text("Lives: " + str(lives), (WIDTH - 110, 8), fontsize=28, color=(220, 220, 220))

    if game_over:
        screen.draw.text("GAME OVER", centerx=WIDTH // 2, centery=HEIGHT // 2 - 20, 
                        fontsize=64, color=(255, 60, 60))
        screen.draw.text("Press R to restart", centerx=WIDTH // 2, centery=HEIGHT // 2 + 40, 
                        fontsize=32, color=(200, 200, 200))


def shoot():
    # bullet spawns at nose of the ship
    bx = player["x"]
    by = player["y"] - player["h"]
    bullets.append({"x": bx, "y": by, "vy": -480})


def player_rect():
    return (player["x"] - player["w"] / 2, player["y"] - player["h"] / 2, player["w"], player["h"])


def collide_circle_rect(cx, cy, r, rect):
    # rect is (x, y, w, h)
    rx, ry, rw, rh = rect
    # find closest point on rect to circle center
    closest_x = clamp(cx, rx, rx + rw)
    closest_y = clamp(cy, ry, ry + rh)
    dx = cx - closest_x
    dy = cy - closest_y
    return dx * dx + dy * dy <= r * r


def collide_circle_point(cx, cy, r, px, py):
    dx = cx - px
    dy = cy - py
    return dx * dx + dy * dy <= r * r


def clamp(v, a, b):
    return max(a, min(b, v))


def on_key_down(key):
    global game_over
    if key == keys.R and game_over:
        restart()


# Start initial spawn timer
last_spawn = time.time()

