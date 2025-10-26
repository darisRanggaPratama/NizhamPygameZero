import pgzrun

# Konstanta layar
WIDTH = 800
HEIGHT = 900

# Warna
BACKGROUND = (240, 240, 240)
TEXT_COLOR = (50, 50, 50)
BOX_COLOR = (220, 220, 220)
HIGHLIGHT_COLOR = (100, 180, 255)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 160, 210)
CORRECT_COLOR = (0, 150, 0)
INCORRECT_COLOR = (150, 0, 0)

# Variabel input dan hasil
input1 = ""
input2 = ""
result = 0
active_input = 1  # 1 untuk input pertama, 2 untuk input kedua
show_visualization = False
animation_progress = 0
animation_speed = 10
show_answer = False
correct = False

# Tombol dan kotak input
input_box1 = Rect(300, 150, 60, 40)
input_box2 = Rect(440, 150, 60, 40)
calculate_button = Rect(350, 220, 100, 40)
answer_button = Rect(350, 280, 100, 40)
button_hovered = False
answer_hovered = False

# Untuk animasi
dots = []
rows_complete = 0
total_rows = 0
current_dot = 0
animation_done = False
animation_timer = 0

def draw():
    screen.fill(BACKGROUND)
    
    # Judul
    screen.draw.text("Belajar Perkalian", midtop=(WIDTH//2, 30), fontsize=36, color=TEXT_COLOR)
    screen.draw.text("Masukkan dua angka untuk dikalikan:", midtop=(WIDTH//2, 100), fontsize=24, color=TEXT_COLOR)
    
    # Kotak input
    box1_color = HIGHLIGHT_COLOR if active_input == 1 else BOX_COLOR
    box2_color = HIGHLIGHT_COLOR if active_input == 2 else BOX_COLOR
    screen.draw.filled_rect(input_box1, box1_color)
    screen.draw.filled_rect(input_box2, box2_color)
    
    # Teks input
    screen.draw.text(input1, center=input_box1.center, fontsize=24, color=TEXT_COLOR)
    screen.draw.text(input2, center=input_box2.center, fontsize=24, color=TEXT_COLOR)
    
    # Tanda perkalian
    screen.draw.text("×", midtop=(400, 155), fontsize=30, color=TEXT_COLOR)
    
    # Tombol hitung
    button_color = BUTTON_HOVER_COLOR if button_hovered else BUTTON_COLOR
    screen.draw.filled_rect(calculate_button, button_color)
    screen.draw.text("Hitung", center=calculate_button.center, fontsize=20, color=(255, 255, 255))

    # Tombol jawab
    answer_color = BUTTON_HOVER_COLOR if answer_hovered else BUTTON_COLOR
    screen.draw.filled_rect(answer_button, answer_color)
    screen.draw.text("Jawab", center=answer_button.center, fontsize=20, color=(255, 255, 255))
    
    # Tampilkan hasil jika sudah dihitung
    if show_visualization:
        screen.draw.text(f"{input1} × {input2} = ?", midtop=(WIDTH//2, 330), fontsize=28, color=TEXT_COLOR)
        
        # Visualisasi perkalian
        draw_visualization()

    # Tampilkan jawaban
    if show_answer:
        answer_text = f"{input1} × {input2} = {result}"
        color = CORRECT_COLOR if correct else INCORRECT_COLOR
        screen.draw.text(answer_text, midtop=(WIDTH//2, 360), fontsize=28, color=color)
    
    # Instruksi
    screen.draw.text("Klik kotak untuk memilih input", midbottom=(WIDTH//2, HEIGHT-10), fontsize=16, color=TEXT_COLOR)
    screen.draw.text("Tekan Enter untuk menghitung", midbottom=(WIDTH//2, HEIGHT-30), fontsize=16, color=TEXT_COLOR)

def draw_visualization():
    global animation_progress, animation_done, current_dot, rows_complete, animation_timer
    
    if not animation_done:
        animation_timer += 1
        
        if animation_timer % 3 == 0 and current_dot < len(dots):
            current_dot += 1
        
        if current_dot >= len(dots):
            animation_done = True
    
    # Gambar semua titik yang sudah muncul dalam animasi
    for i, dot in enumerate(dots[:current_dot]):
        x, y, row = dot
        color = (50, 100, 200) if i % int(input2) < rows_complete else (200, 50, 50)
        screen.draw.filled_circle((x, y), 8, color)
    
    # Garis untuk memisahkan baris
    if int(input2) > 0:
        completed_rows = min(rows_complete, int(input2))
        for i in range(1, completed_rows + 1):
            y = 400 + i * 25
            screen.draw.line((200, y), (600, y), (200, 200, 200))
    
    # Tambah jumlah baris yang selesai setelah delay
    if animation_timer % 15 == 0 and rows_complete < int(input2) and animation_progress > 0.3:
        rows_complete += 1
    
    # Tambahkan penjelasan
    if rows_complete > 0:
        for i in range(min(rows_complete, int(input2))):
            screen.draw.text(f"{input1} × {i+1} = {int(input1) * (i+1)}", 
                             topleft=(620, 400 + i * 25), fontsize=20, color=TEXT_COLOR)

def on_mouse_down(pos):
    global active_input, show_visualization, animation_progress
    global dots, rows_complete, current_dot, animation_done, animation_timer
    global show_answer
    
    # Cek jika klik pada kotak input
    if input_box1.collidepoint(pos):
        active_input = 1
    elif input_box2.collidepoint(pos):
        active_input = 2
    # Cek jika klik pada tombol hitung
    elif calculate_button.collidepoint(pos):
        calculate()
    # Cek jika klik pada tombol jawab
    elif answer_button.collidepoint(pos):
        show_answer = True
        check_answer()

def on_mouse_move(pos):
    global button_hovered, answer_hovered
    button_hovered = calculate_button.collidepoint(pos)
    answer_hovered = answer_button.collidepoint(pos)

def on_key_down(key):
    global input1, input2, active_input, show_answer
    
    if key == keys.RETURN:
        calculate()
    elif key == keys.BACKSPACE:
        if active_input == 1 and input1:
            input1 = input1[:-1]
        elif active_input == 2 and input2:
            input2 = input2[:-1]
    elif key == keys.TAB:
        active_input = 2 if active_input == 1 else 1
    else:
        # Hanya terima angka 0-9 dan batasi panjang input
        if key in (keys.K_0, keys.K_1, keys.K_2, keys.K_3, keys.K_4, 
                  keys.K_5, keys.K_6, keys.K_7, keys.K_8, keys.K_9):
            if active_input == 1 and len(input1) < 2:
                input1 += key.name[-1]  # Ambil karakter terakhir dari key.name
            elif active_input == 2 and len(input2) < 2:
                input2 += key.name[-1]
    
    show_answer = False

def calculate():
    global result, show_visualization, animation_progress
    global dots, rows_complete, current_dot, animation_done, animation_timer
    global show_answer
    
    # Pastikan input valid
    if input1.isdigit() and input2.isdigit():
        num1 = int(input1)
        num2 = int(input2)
        result = num1 * num2
        show_visualization = True
        animation_progress = 0
        show_answer = False
        
        # Reset animasi
        dots = []
        rows_complete = 0
        current_dot = 0
        animation_done = False
        animation_timer = 0
        
        # Buat titik-titik untuk visualisasi
        for j in range(num2):
            for i in range(num1):
                x = 250 + i * 30
                y = 400 + j * 25
                dots.append((x, y, j))
        
        # Batasi jumlah titik
        if len(dots) > 300:
            dots = dots[:300]
        
        total_rows = num2

def check_answer():
    global correct
    if input1.isdigit() and input2.isdigit():
        num1 = int(input1)
        num2 = int(input2)
        correct_answer = num1 * num2
        correct = result == correct_answer
    else:
        correct = False

def update():
    global animation_progress
    if show_visualization and animation_progress < 1:
        animation_progress += 0.01 * animation_speed

pgzrun.go()