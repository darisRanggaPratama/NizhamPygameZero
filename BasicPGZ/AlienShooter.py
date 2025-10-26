import pgzrun
import random
from pgzero.actor import Actor
from pgzero.keyboard import keyboard
from pgzero.clock import clock

# Inisialisasi objek game
TITLE = "Alien Shooter"  # Judul window game
FPS = 60  # Set frame rate ke 60 FPS

# Window settings
WIDTH = 800  # Ukuran window yang lebih kecil agar bisa di tengah
HEIGHT = 600
CENTERX = WIDTH // 2
CENTERY = HEIGHT // 2

# Inisialisasi game objects
player = Actor('player', (CENTERX, HEIGHT - 50), anchor=('center', 'center'))
player.scale = 0.01  # Memperkecil ukuran player menjadi 1%
aliens = []
bullets = []
score = 0


def update():
    global score
    # Kontrol pemain dengan delta time untuk pergerakan yang lebih halus
    dt = 1/60  # Delta time untuk 60 FPS
    if keyboard.left and player.x > 20:
        player.x -= 300 * dt  # 300 pixels per second
    if keyboard.right and player.x < WIDTH - 20:
        player.x += 300 * dt  # 300 pixels per second
    if keyboard.space:
        bullet = Actor('bullet', (player.x, player.y - 60), anchor=('center', 'center'))
        bullet.scale = 0.01  # Memperkecil ukuran peluru menjadi 1%
        bullets.append(bullet)
        clock.schedule_unique(lambda: None, 1)  # Cooldown 1 detik antara tembakan

    # Update bullets dengan delta time untuk pergerakan yang lebih halus
    for bullet in bullets[:]:
        bullet.y -= 300 * dt  # Mengurangi kecepatan peluru agar tidak berbayang
        if bullet.y < 0:
            bullets.remove(bullet)

    # Spawn aliens
    if random.randint(1, 30) == 1:
        alien = Actor('monster', (random.randint(50, WIDTH - 50), -50), anchor=('center', 'center'))
        alien.scale = 0.01  # Memperkecil ukuran alien menjadi 1%
        aliens.append(alien)

    # Update aliens dengan delta time untuk pergerakan yang lebih halus
    for alien in aliens[:]:
        alien.y += 180 * dt  # 180 pixels per second
        if alien.y > HEIGHT:
            aliens.remove(alien)
        
    # Collision detection
    for bullet in bullets[:]:
        hit = False
        for alien in aliens[:]:
            if bullet.colliderect(alien):
                bullets.remove(bullet)
                aliens.remove(alien)
                score += 10
                hit = True
                break  # Keluar dari loop alien setelah bullet mengenai satu alien
        if hit:
            continue  # Lanjut ke bullet berikutnya


def draw():
    # Bersihkan layar dengan benar-benar menghapus semua konten
    screen.clear()
    screen.fill((0, 0, 0))  # Menggunakan RGB untuk warna hitam
    
    # Gambar semua objek game
    player.draw()
    
    # Gambar peluru yang aktif
    for bullet in bullets:
        bullet.draw()
    
    # Gambar alien yang aktif    
    for alien in aliens:
        alien.draw()
    
    # Gambar skor
    screen.draw.text(f'Score: {score}', (10, 10), color='white', fontsize=30)


# Jalankan game
pgzrun.go()
