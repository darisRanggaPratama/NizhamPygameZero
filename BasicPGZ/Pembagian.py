import pgzrun
import random

# Konfigurasi layar
WIDTH = 800
HEIGHT = 950
TITLE = "Belajar Pembagian dengan Visual"

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

# Game state
state = "menu"  # menu, playing, result
dividend = 12  # Angka yang dibagi
divisor = 3  # Pembagi
player_answer = ""
correct_answer = 0
score = 0
total_questions = 0
show_hint = False
animation_progress = 0


def generate_question():
    global dividend, divisor, correct_answer, player_answer, show_hint, animation_progress
    # Generate soal yang habis dibagi
    divisor = random.randint(2, 6)
    quotient = random.randint(2, 8)
    dividend = divisor * quotient
    correct_answer = quotient
    player_answer = ""
    show_hint = False
    animation_progress = 0


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
    screen.draw.text("BELAJAR PEMBAGIAN",
                     center=(WIDTH // 2, 100),
                     fontsize=60, color=BLUE)
    screen.draw.text("dengan Visual",
                     center=(WIDTH // 2, 150),
                     fontsize=40, color=PURPLE)

    # Instruksi
    screen.draw.text("Tekan SPASI untuk mulai",
                     center=(WIDTH // 2, 300),
                     fontsize=35, color=GREEN)
    screen.draw.text("Tekan H untuk melihat hint",
                     center=(WIDTH // 2, 350),
                     fontsize=25, color=ORANGE)

    # Info konsep
    screen.draw.text("Pembagian = Membagi sama rata",
                     center=(WIDTH // 2, 420),
                     fontsize=23, color=PURPLE)

    # Skor
    screen.draw.text(f"Skor: {score}/{total_questions}",
                     center=(WIDTH // 2, 480),
                     fontsize=30, color=BLACK)


def draw_game():
    # Soal
    screen.draw.text(f"{dividend} ÷ {divisor} = ?",
                     center=(WIDTH // 2, 40),
                     fontsize=50, color=BLUE)

    screen.draw.text(f"Bagi {dividend} kue ke {divisor} piring",
                     center=(WIDTH // 2, 90),
                     fontsize=25, color=PURPLE)

    # Visualisasi pembagian
    start_y = 140

    # Gambar semua kue di atas (yang akan dibagi)
    cake_size = 30
    cakes_per_row = 12
    cake_spacing = 10

    total_width = min(dividend, cakes_per_row) * (cake_size + cake_spacing)
    start_x = (WIDTH - total_width) // 2

    # Kue yang belum dibagi
    screen.draw.text("Kue yang akan dibagi:",
                     (start_x, start_y),
                     fontsize=22, color=ORANGE)

    for i in range(dividend):
        row = i // cakes_per_row
        col = i % cakes_per_row
        x = start_x + col * (cake_size + cake_spacing)
        y = start_y + 35 + row * (cake_size + cake_spacing)

        # Gambar kue (lingkaran)
        screen.draw.filled_circle((x + cake_size // 2, y + cake_size // 2),
                                  cake_size // 2, YELLOW)
        screen.draw.circle((x + cake_size // 2, y + cake_size // 2),
                           cake_size // 2, ORANGE)

    # Visualisasi hasil pembagian ke piring
    plate_y = start_y + 35 + ((dividend - 1) // cakes_per_row + 1) * (cake_size + cake_spacing) + 50

    screen.draw.text("Dibagi ke piring:",
                     (start_x, plate_y),
                     fontsize=22, color=GREEN)

    plate_size = 80
    plate_spacing = 20
    plates_start_x = (WIDTH - divisor * (plate_size + plate_spacing)) // 2

    # Gambar piring-piring
    for i in range(divisor):
        plate_x = plates_start_x + i * (plate_size + plate_spacing)
        plate_center_x = plate_x + plate_size // 2
        plate_center_y = plate_y + 60

        # Piring (oval)
        screen.draw.filled_circle((plate_center_x, plate_center_y),
                                  plate_size // 2, LIGHT_BLUE)
        screen.draw.circle((plate_center_x, plate_center_y),
                           plate_size // 2, BLUE)

        screen.draw.text(f"Piring {i + 1}",
                         center=(plate_center_x, plate_center_y + plate_size // 2 + 15),
                         fontsize=16, color=BLACK)

    # Hint - tampilkan pembagian kue ke piring
    if show_hint:
        hint_y = plate_y + 140
        screen.draw.text("💡 Setiap piring mendapat kue yang sama!",
                         center=(WIDTH // 2, hint_y),
                         fontsize=23, color=PURPLE)

        # Gambar kue kecil di setiap piring
        for plate_idx in range(divisor):
            plate_x = plates_start_x + plate_idx * (plate_size + plate_spacing)
            plate_center_x = plate_x + plate_size // 2
            plate_center_y = plate_y + 60

            # Hitung jumlah kue per piring
            cakes_per_plate = correct_answer

            # Gambar kue kecil di piring
            for cake_idx in range(cakes_per_plate):
                mini_cake_size = 12
                angle = (360 / cakes_per_plate) * cake_idx
                import math
                offset_x = math.cos(math.radians(angle)) * 20
                offset_y = math.sin(math.radians(angle)) * 20

                cake_x = plate_center_x + offset_x
                cake_y = plate_center_y + offset_y

                screen.draw.filled_circle((int(cake_x), int(cake_y)),
                                          mini_cake_size // 2, YELLOW)
                screen.draw.circle((int(cake_x), int(cake_y)),
                                   mini_cake_size // 2, ORANGE)

        screen.draw.text(f"Setiap piring dapat {correct_answer} kue",
                         center=(WIDTH // 2, hint_y + 30),
                         fontsize=23, color=GREEN)

    # Input jawaban
    answer_y = HEIGHT - 100
    screen.draw.text("Berapa kue per piring?",
                     center=(WIDTH // 2, answer_y - 30),
                     fontsize=25, color=BLACK)

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
                     center=(WIDTH // 2, 120),
                     fontsize=60, color=bg_color)

    # Penjelasan
    screen.draw.text(f"{dividend} ÷ {divisor} = {correct_answer}",
                     center=(WIDTH // 2, 200),
                     fontsize=45, color=BLUE)

    if player_answer != str(correct_answer):
        screen.draw.text(f"Jawaban kamu: {player_answer}",
                         center=(WIDTH // 2, 250),
                         fontsize=32, color=RED)

    # Visualisasi penjelasan
    screen.draw.text(f"{emoji} {dividend} kue dibagi ke {divisor} piring",
                     center=(WIDTH // 2, 310),
                     fontsize=27, color=PURPLE)
    screen.draw.text(f"Setiap piring mendapat {correct_answer} kue",
                     center=(WIDTH // 2, 345),
                     fontsize=27, color=GREEN)

    # Konsep tambahan
    screen.draw.text(f"Cek: {correct_answer} × {divisor} = {dividend} ✓",
                     center=(WIDTH // 2, 395),
                     fontsize=24, color=ORANGE)

    # Instruksi lanjut
    screen.draw.text("Tekan SPASI untuk soal berikutnya",
                     center=(WIDTH // 2, 470),
                     fontsize=28, color=GREEN)
    screen.draw.text("Tekan ESC untuk ke menu",
                     center=(WIDTH // 2, 505),
                     fontsize=23, color=ORANGE)

    # Skor
    screen.draw.text(f"Skor: {score}/{total_questions}",
                     center=(WIDTH // 2, HEIGHT - 30),
                     fontsize=28, color=BLACK)


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
            if len(player_answer) < 2:
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