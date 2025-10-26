import pgzrun
import random

# Konfigurasi layar
WIDTH = 800
HEIGHT = 900
TITLE = "Belajar Perkalian dengan Visual"

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (52, 152, 219)
GREEN = (46, 204, 113)
RED = (231, 76, 60)
YELLOW = (241, 196, 15)
PURPLE = (155, 89, 182)
ORANGE = (230, 126, 34)

# Game state
state = "menu"  # menu, playing, result
num1 = 3
num2 = 4
player_answer = ""
correct_answer = 0
score = 0
total_questions = 0
show_hint = False


def generate_question():
    global num1, num2, correct_answer, player_answer, show_hint
    num1 = random.randint(2, 9)
    num2 = random.randint(2, 9)
    correct_answer = num1 * num2
    player_answer = ""
    show_hint = False


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
    screen.draw.text("BELAJAR PERKALIAN",
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

    # Info
    screen.draw.text(f"Skor: {score}/{total_questions}",
                     center=(WIDTH // 2, 450),
                     fontsize=30, color=BLACK)


def draw_game():
    # Soal
    screen.draw.text(f"{num1} × {num2} = ?",
                     center=(WIDTH // 2, 50),
                     fontsize=50, color=BLUE)

    # Visualisasi perkalian sebagai array (baris x kolom)
    start_x = 150
    start_y = 120
    box_size = 40
    spacing = 10

    # Gambar grid representasi perkalian
    for row in range(num1):
        for col in range(num2):
            x = start_x + col * (box_size + spacing)
            y = start_y + row * (box_size + spacing)

            # Kotak berwarna
            screen.draw.filled_rect(
                Rect(x, y, box_size, box_size),
                YELLOW
            )
            screen.draw.rect(
                Rect(x, y, box_size, box_size),
                ORANGE
            )

    # Label baris dan kolom
    screen.draw.text(f"{num1} baris",
                     (start_x, start_y + num1 * (box_size + spacing) + 20),
                     fontsize=25, color=RED)
    screen.draw.text(f"{num2} kolom",
                     (start_x + num2 * (box_size + spacing) + 20, start_y + 20),
                     fontsize=25, color=BLUE, angle=90)

    # Hint
    if show_hint:
        hint_y = start_y + num1 * (box_size + spacing) + 70
        screen.draw.text("Hitung semua kotak:",
                         (WIDTH // 2 - 150, hint_y),
                         fontsize=25, color=PURPLE)

        # Tampilkan perhitungan
        calc_text = ""
        for i in range(num1):
            calc_text += f"{num2}"
            if i < num1 - 1:
                calc_text += " + "

        screen.draw.text(calc_text + f" = {correct_answer}",
                         (WIDTH // 2 - 150, hint_y + 35),
                         fontsize=25, color=GREEN)

    # Input jawaban
    answer_y = HEIGHT - 150
    screen.draw.text("Jawaban Kamu:",
                     center=(WIDTH // 2, answer_y),
                     fontsize=30, color=BLACK)

    # Kotak input
    input_box = Rect(WIDTH // 2 - 100, answer_y + 40, 200, 50)
    screen.draw.filled_rect(input_box, (240, 240, 240))
    screen.draw.rect(input_box, BLUE)

    screen.draw.text(player_answer if player_answer else "_",
                     center=(WIDTH // 2, answer_y + 65),
                     fontsize=40, color=BLACK)

    # Instruksi
    screen.draw.text("Ketik angka lalu tekan ENTER",
                     center=(WIDTH // 2, HEIGHT - 50),
                     fontsize=20, color=(100, 100, 100))
    screen.draw.text("Tekan H untuk hint",
                     center=(WIDTH // 2, HEIGHT - 25),
                     fontsize=18, color=ORANGE)


def draw_result():
    # Background
    if player_answer == str(correct_answer):
        bg_color = GREEN
        result_text = "BENAR! 🎉"
    else:
        bg_color = RED
        result_text = "BELUM TEPAT"

    screen.draw.filled_rect(Rect(0, 0, WIDTH, HEIGHT), WHITE)

    # Hasil
    screen.draw.text(result_text,
                     center=(WIDTH // 2, 150),
                     fontsize=60, color=bg_color)

    # Penjelasan
    screen.draw.text(f"{num1} × {num2} = {correct_answer}",
                     center=(WIDTH // 2, 250),
                     fontsize=45, color=BLUE)

    if player_answer != str(correct_answer):
        screen.draw.text(f"Jawaban kamu: {player_answer}",
                         center=(WIDTH // 2, 310),
                         fontsize=35, color=RED)

    # Visualisasi singkat
    screen.draw.text(f"{num1} baris × {num2} kolom = {num1 * num2} kotak",
                     center=(WIDTH // 2, 370),
                     fontsize=30, color=PURPLE)

    # Instruksi lanjut
    screen.draw.text("Tekan SPASI untuk soal berikutnya",
                     center=(WIDTH // 2, 470),
                     fontsize=30, color=GREEN)
    screen.draw.text("Tekan ESC untuk ke menu",
                     center=(WIDTH // 2, 510),
                     fontsize=25, color=ORANGE)

    # Skor
    screen.draw.text(f"Skor: {score}/{total_questions}",
                     center=(WIDTH // 2, HEIGHT - 40),
                     fontsize=30, color=BLACK)


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