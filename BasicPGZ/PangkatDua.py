import pgzrun
import random

# Konfigurasi layar
WIDTH = 800
HEIGHT = 950
TITLE = "Belajar Pangkat 2 dengan Visual"

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

# Game state
state = "menu"  # menu, playing, result
base_number = 3  # Angka yang dipangkatkan
player_answer = ""
correct_answer = 0
score = 0
total_questions = 0
show_hint = False
animation_frame = 0


def generate_question():
    global base_number, correct_answer, player_answer, show_hint, animation_frame
    base_number = random.randint(2, 12)
    correct_answer = base_number ** 2
    player_answer = ""
    show_hint = False
    animation_frame = 0


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
    screen.draw.text("BELAJAR PANGKAT 2",
                     center=(WIDTH // 2, 90),
                     fontsize=60, color=BLUE)
    screen.draw.text("dengan Visual",
                     center=(WIDTH // 2, 140),
                     fontsize=40, color=PURPLE)

    # Penjelasan konsep
    screen.draw.text("Pangkat 2 = Kuadrat = Persegi",
                     center=(WIDTH // 2, 220),
                     fontsize=28, color=DARK_BLUE)

    # Contoh visual kecil
    example_size = 40
    example_x = WIDTH // 2 - 120
    example_y = 270

    screen.draw.text("Contoh: 3² =",
                     (example_x - 20, example_y-20),
                     fontsize=25, color=ORANGE)

    # Gambar grid 3x3
    for row in range(3):
        for col in range(3):
            x = example_x + col * (example_size + 5)
            y = example_y + row * (example_size + 5)
            screen.draw.filled_rect(Rect(x, y, example_size, example_size), YELLOW)
            screen.draw.rect(Rect(x, y, example_size, example_size), ORANGE)

    screen.draw.text("= 9",
                     (example_x + 180, example_y + 30),
                     fontsize=25, color=GREEN)

    screen.draw.text("3 baris × 3 kolom = 9 kotak",
                     center=(WIDTH // 2, example_y + 160),
                     fontsize=22, color=PURPLE)

    # Instruksi
    screen.draw.text("Tekan SPASI untuk mulai",
                     center=(WIDTH // 2, 450),
                     fontsize=35, color=GREEN)
    screen.draw.text("Tekan H untuk melihat hint",
                     center=(WIDTH // 2, 495),
                     fontsize=25, color=ORANGE)

    # Skor
    screen.draw.text(f"Skor: {score}/{total_questions}",
                     center=(WIDTH // 2, HEIGHT - 30),
                     fontsize=28, color=BLACK)


def draw_game():
    # Soal
    screen.draw.text(f"{base_number}² = ?",
                     center=(WIDTH // 2, 40),
                     fontsize=55, color=BLUE)

    screen.draw.text(f"({base_number} pangkat 2 = {base_number} × {base_number})",
                     center=(WIDTH // 2, 85),
                     fontsize=24, color=PURPLE)

    # Visualisasi sebagai persegi/kuadrat
    square_start_y = 130

    # Hitung ukuran kotak agar pas di layar
    max_square_size = 400
    box_size = min(30, max_square_size // base_number)
    spacing = 2

    total_size = base_number * (box_size + spacing) - spacing
    square_start_x = (WIDTH - total_size) // 2

    # Label atas
    screen.draw.text(f"{base_number} kolom →",
                     center=(WIDTH // 2, square_start_y - 25),
                     fontsize=22, color=BLUE)

    # Gambar grid persegi
    colors = [YELLOW, PINK, LIGHT_BLUE, (144, 238, 144), (255, 218, 185)]

    for row in range(base_number):
        for col in range(base_number):
            x = square_start_x + col * (box_size + spacing)
            y = square_start_y + row * (box_size + spacing)

            # Pilih warna untuk membuat pola
            color_index = (row + col) % len(colors)
            box_color = colors[color_index]

            screen.draw.filled_rect(Rect(x, y, box_size, box_size), box_color)
            screen.draw.rect(Rect(x, y, box_size, box_size), ORANGE)

    # Label samping
    label_x = square_start_x - 80
    label_y = square_start_y + total_size // 2
    screen.draw.text(f"{base_number}",
                     center=(label_x, label_y - 15),
                     fontsize=22, color=RED)
    screen.draw.text("baris",
                     center=(label_x, label_y + 10),
                     fontsize=18, color=RED)
    screen.draw.text("↓",
                     center=(label_x, label_y + 35),
                     fontsize=22, color=RED)

    # Info di bawah grid
    info_y = square_start_y + total_size + 30

    screen.draw.text(f"Persegi dengan sisi {base_number}",
                     center=(WIDTH // 2, info_y),
                     fontsize=24, color=DARK_BLUE)

    # Hint
    if show_hint:
        hint_y = info_y + 40
        screen.draw.text("💡 Hitung semua kotak dalam persegi!",
                         center=(WIDTH // 2, hint_y),
                         fontsize=23, color=PURPLE)

        screen.draw.text(f"{base_number} × {base_number} = {correct_answer} kotak",
                         center=(WIDTH // 2, hint_y + 35),
                         fontsize=26, color=GREEN)

        # Rumus tambahan
        screen.draw.text(f"Atau: ",
                         (WIDTH // 2 - 130, hint_y + 70),
                         fontsize=22, color=ORANGE)

        # Tampilkan penjumlahan berulang
        sum_text = " + ".join([str(base_number)] * base_number)
        if len(sum_text) > 50:
            sum_text = f" {base_number} dijumlahkan {base_number} kali"
        screen.draw.text(f"{sum_text} = {correct_answer}",
                         (WIDTH // 2 - 80, hint_y + 70),
                         fontsize=20, color=ORANGE)

    # Input jawaban
    answer_y = HEIGHT - 100
    screen.draw.text("Jawaban:",
                     center=(WIDTH // 2, answer_y - 25),
                     fontsize=26, color=BLACK)

    # Kotak input
    input_box = Rect(WIDTH // 2 - 90, answer_y, 180, 45)
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
                     center=(WIDTH // 2, 100),
                     fontsize=60, color=bg_color)

    # Penjelasan
    screen.draw.text(f"{base_number}² = {correct_answer}",
                     center=(WIDTH // 2, 180),
                     fontsize=50, color=BLUE)

    if player_answer != str(correct_answer):
        screen.draw.text(f"Jawaban kamu: {player_answer}",
                         center=(WIDTH // 2, 235),
                         fontsize=32, color=RED)

    # Visualisasi penjelasan
    screen.draw.text(f"{emoji} {base_number} pangkat 2 artinya {base_number} × {base_number}",
                     center=(WIDTH // 2, 290),
                     fontsize=25, color=PURPLE)

    # Gambar persegi kecil sebagai penjelasan
    mini_size = 25
    mini_spacing = 3
    mini_total = base_number * (mini_size + mini_spacing)
    mini_x = (WIDTH - mini_total) // 2
    mini_y = 330

    for row in range(base_number):
        for col in range(base_number):
            x = mini_x + col * (mini_size + mini_spacing)
            y = mini_y + row * (mini_size + mini_spacing)
            screen.draw.filled_rect(Rect(x, y, mini_size, mini_size), YELLOW)
            screen.draw.rect(Rect(x, y, mini_size, mini_size), ORANGE)

    screen.draw.text(f"Persegi {base_number}×{base_number} = {correct_answer} kotak",
                     center=(WIDTH // 2, mini_y + mini_total + 25),
                     fontsize=24, color=GREEN)

    # Fakta menarik
    if base_number <= 10:
        screen.draw.text(f"📚 Ini disebut '{base_number} kuadrat'",
                         center=(WIDTH // 2, mini_y + mini_total + 60),
                         fontsize=22, color=DARK_BLUE)

    # Instruksi lanjut
    screen.draw.text("Tekan SPASI untuk soal berikutnya",
                     center=(WIDTH // 2, HEIGHT - 80),
                     fontsize=28, color=GREEN)
    screen.draw.text("Tekan ESC untuk ke menu",
                     center=(WIDTH // 2, HEIGHT - 50),
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
            if len(player_answer) < 4:
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