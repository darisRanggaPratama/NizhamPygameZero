import pgzrun
import random
import math

# Konfigurasi layar
WIDTH = 800
HEIGHT = 950
TITLE = "Belajar Akar Pangkat 2 dengan Visual"

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (52, 152, 219)
GREEN = (46, 204, 113)
RED = (231, 76, 60)
YELLOW = (241, 196, 15)
PURPLE = (155, 89, 182)
ORANGE = (230, 126, 34)
PINK = (255, 182, 193)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (41, 128, 185)
LIGHT_GREEN = (144, 238, 144)

# Game state
state = "menu"  # menu, playing, result
number = 16  # Angka yang akan dicari akarnya
player_answer = ""
correct_answer = 0
score = 0
total_questions = 0
show_hint = False
animation_stage = 0

# Daftar bilangan kuadrat sempurna untuk soal
perfect_squares = [4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144]


def generate_question():
    global number, correct_answer, player_answer, show_hint, animation_stage
    number = random.choice(perfect_squares)
    correct_answer = int(math.sqrt(number))
    player_answer = ""
    show_hint = False
    animation_stage = 0


def draw():
    screen.clear()
    screen.fill(WHITE)

    if state == "menu":
        draw_menu()
    elif state == "playing":
        draw_game()
    elif state == "result":
        draw_result()


def draw_menu():
    # Judul
    screen.draw.text("BELAJAR AKAR PANGKAT 2",
                     center=(WIDTH // 2, 80),
                     fontsize=55, color=BLUE)
    screen.draw.text("dengan Visual",
                     center=(WIDTH // 2, 130),
                     fontsize=40, color=PURPLE)

    # Penjelasan konsep
    screen.draw.text("Akar Pangkat 2 = Kebalikan dari Pangkat 2",
                     center=(WIDTH // 2, 200),
                     fontsize=26, color=DARK_BLUE)

    # Contoh visual
    example_y = 250

    screen.draw.text("Contoh:",
                     center=(WIDTH // 2, example_y),
                     fontsize=24, color=ORANGE)

    # Persegi 4x4
    box_size = 30
    grid_size = 4
    total_boxes = grid_size * grid_size
    start_x = WIDTH // 2 - (grid_size * (box_size + 3)) // 2
    start_y = example_y + 10

    for row in range(grid_size):
        for col in range(grid_size):
            x = start_x + col * (box_size + 3)
            y = start_y + row * (box_size + 3)
            screen.draw.filled_rect(Rect(x, y, box_size, box_size), YELLOW)
            screen.draw.rect(Rect(x, y, box_size, box_size), ORANGE)

    # Penjelasan
    screen.draw.text(f"√{total_boxes} = {grid_size}",
                     center=(WIDTH // 2, start_y + grid_size * (box_size + 3) + 25),
                     fontsize=28, color=GREEN)

    screen.draw.text(f"{total_boxes} kotak → Persegi sisi {grid_size}",
                     center=(WIDTH // 2, start_y + grid_size * (box_size + 3) + 60),
                     fontsize=22, color=PURPLE)

    # Instruksi
    screen.draw.text("Tekan SPASI untuk mulai",
                     center=(WIDTH // 2, 480),
                     fontsize=35, color=GREEN)
    screen.draw.text("Tekan H untuk melihat hint",
                     center=(WIDTH // 2, 520),
                     fontsize=25, color=ORANGE)

    # Skor
    screen.draw.text(f"Skor: {score}/{total_questions}",
                     center=(WIDTH // 2, HEIGHT - 20),
                     fontsize=26, color=BLACK)


def draw_game():
    # Soal
    screen.draw.text(f"√{number} = ?",
                     center=(WIDTH // 2, 40),
                     fontsize=55, color=BLUE)

    screen.draw.text(f"(Akar dari {number})",
                     center=(WIDTH // 2, 85),
                     fontsize=24, color=PURPLE)

    # Visualisasi: Tampilkan kotak-kotak yang akan disusun jadi persegi
    visual_y = 130

    screen.draw.text(f"Susun {number} kotak menjadi persegi:",
                     center=(WIDTH // 2, visual_y),
                     fontsize=23, color=DARK_BLUE)

    # Hitung ukuran grid
    side = int(math.sqrt(number))
    box_size = min(35, 300 // side)
    spacing = 2

    total_size = side * (box_size + spacing) - spacing
    grid_x = (WIDTH - total_size) // 2
    grid_y = visual_y + 40

    # Gambar grid persegi
    colors = [YELLOW, LIGHT_GREEN, LIGHT_BLUE, PINK, (255, 218, 185)]

    for row in range(side):
        for col in range(side):
            x = grid_x + col * (box_size + spacing)
            y = grid_y + row * (box_size + spacing)

            box_num = row * side + col
            color_index = box_num % len(colors)

            screen.draw.filled_rect(Rect(x, y, box_size, box_size), colors[color_index])
            screen.draw.rect(Rect(x, y, box_size, box_size), ORANGE)

    # Tanda panah dan label
    arrow_y = grid_y + total_size // 2

    # Label kiri
    screen.draw.text(f"? ",
                     (grid_x - 50, arrow_y - 20),
                     fontsize=30, color=RED)
    screen.draw.text("kotak",
                     (grid_x - 60, arrow_y + 10),
                     fontsize=18, color=RED)

    # Label atas
    screen.draw.text(f"? kotak",
                     center=(WIDTH // 2, grid_y - 25),
                     fontsize=20, color=BLUE)

    # Info di bawah
    info_y = grid_y + total_size + 45
    screen.draw.text(f"Total: {number} kotak dalam persegi",
                     center=(WIDTH // 2, info_y),
                     fontsize=24, color=PURPLE)

    # Hint
    if show_hint:
        hint_y = info_y + 45

        screen.draw.text("💡 Cari sisi persegi yang pas!",
                         center=(WIDTH // 2, hint_y),
                         fontsize=23, color=PURPLE)

        screen.draw.text(f"Persegi dengan sisi {correct_answer} × {correct_answer} = {number}",
                         center=(WIDTH // 2, hint_y + 35),
                         fontsize=24, color=GREEN)

        screen.draw.text(f"Jadi √{number} = {correct_answer}",
                         center=(WIDTH // 2, hint_y + 70),
                         fontsize=26, color=ORANGE)

    # Input jawaban
    answer_y = HEIGHT - 100
    screen.draw.text("Berapa panjang sisi persegi?",
                     center=(WIDTH // 2, answer_y - 25),
                     fontsize=24, color=BLACK)

    # Kotak input
    input_box = Rect(WIDTH // 2 - 80, answer_y, 160, 45)
    screen.draw.filled_rect(input_box, (240, 240, 240))
    screen.draw.rect(input_box, BLUE)

    screen.draw.text(player_answer if player_answer else "_",
                     center=(WIDTH // 2, answer_y + 22),
                     fontsize=35, color=BLACK)

    # Instruksi
    screen.draw.text("Ketik angka lalu tekan ENTER | Tekan H untuk hint",
                     center=(WIDTH // 2, HEIGHT - 25),
                     fontsize=18, color=(100, 100, 100))


def draw_result():
    # Background
    if player_answer == str(correct_answer):
        bg_color = GREEN
        result_text = "BENAR! 🎉"
        emoji = "✨"
    else:
        bg_color = RED
        result_text = "BELUM TEPAT"
        emoji = "💭"

    screen.draw.filled_rect(Rect(0, 0, WIDTH, HEIGHT), WHITE)

    # Hasil
    screen.draw.text(result_text,
                     center=(WIDTH // 2, 90),
                     fontsize=60, color=bg_color)

    # Penjelasan
    screen.draw.text(f"√{number} = {correct_answer}",
                     center=(WIDTH // 2, 170),
                     fontsize=50, color=BLUE)

    if player_answer != str(correct_answer):
        screen.draw.text(f"Jawaban kamu: {player_answer}",
                         center=(WIDTH // 2, 220),
                         fontsize=32, color=RED)

    # Visualisasi penjelasan
    explain_y = 270
    screen.draw.text(f"{emoji} Akar dari {number} adalah {correct_answer}",
                     center=(WIDTH // 2, explain_y),
                     fontsize=25, color=PURPLE)

    # Gambar persegi sebagai bukti
    side = correct_answer
    mini_size = min(25, 200 // side)
    mini_spacing = 2
    mini_total = side * (mini_size + mini_spacing)
    mini_x = (WIDTH - mini_total) // 2
    mini_y = explain_y + 45

    for row in range(side):
        for col in range(side):
            x = mini_x + col * (mini_size + mini_spacing)
            y = mini_y + row * (mini_size + mini_spacing)
            screen.draw.filled_rect(Rect(x, y, mini_size, mini_size), YELLOW)
            screen.draw.rect(Rect(x, y, mini_size, mini_size), ORANGE)

    # Penjelasan lengkap
    screen.draw.text(f"Karena {correct_answer} × {correct_answer} = {number}",
                     center=(WIDTH // 2, mini_y + mini_total + 25),
                     fontsize=24, color=GREEN)

    # Hubungan dengan pangkat 2
    screen.draw.text(f"📐 {correct_answer}² = {number}, maka √{number} = {correct_answer}",
                     center=(WIDTH // 2, mini_y + mini_total + 60),
                     fontsize=22, color=DARK_BLUE)

    # Instruksi lanjut
    screen.draw.text("Tekan SPASI untuk soal berikutnya",
                     center=(WIDTH // 2, HEIGHT - 75),
                     fontsize=28, color=GREEN)
    screen.draw.text("Tekan ESC untuk ke menu",
                     center=(WIDTH // 2, HEIGHT - 45),
                     fontsize=23, color=ORANGE)

    # Skor
    screen.draw.text(f"Skor: {score}/{total_questions}",
                     center=(WIDTH // 2, HEIGHT - 15),
                     fontsize=26, color=BLACK)


def on_key_down(key):
    global state, player_answer, score, total_questions, show_hint

    if state == "menu":
        if key == keys.SPACE:
            state = "playing"
            generate_question()

    elif state == "playing":
        # Toggle hint
        if key == keys.H:
            show_hint = not show_hint

        # Input angka
        elif key in [keys.K_0, keys.K_1, keys.K_2, keys.K_3, keys.K_4,
                     keys.K_5, keys.K_6, keys.K_7, keys.K_8, keys.K_9]:
            if len(player_answer) < 3:
                player_answer += key.name[-1]

        # Hapus
        elif key == keys.BACKSPACE:
            player_answer = player_answer[:-1]

        # Submit jawaban
        elif key == keys.RETURN and player_answer:
            total_questions += 1
            if player_answer == str(correct_answer):
                score += 1
            state = "result"

    elif state == "result":
        if key == keys.SPACE:
            state = "playing"
            generate_question()
        elif key == keys.ESCAPE:
            state = "menu"


# Generate soal pertama
generate_question()

pgzrun.go()