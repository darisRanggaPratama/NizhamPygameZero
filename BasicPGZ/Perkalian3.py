import pgzrun

# Lebar dan tinggi layar
WIDTH = 800
HEIGHT = 600

# Variabel untuk faktor perkalian
factor1 = 1  # Angka pertama, default 1
factor2 = 1  # Angka kedua, default 1
input_mode = 1  # 1: input factor1, 2: input factor2
result = 1  # Default hasil

# Ukuran grid untuk visualisasi
cell_size = 40
grid_x = 50
grid_y = 120


def draw():
    screen.clear()
    screen.fill((255, 255, 255))  # Latar belakang putih

    # Tampilkan instruksi
    screen.draw.text("Masukkan angka pertama (1-10, 0=10): " + str(factor1), (50, 50), color="black", fontsize=30)
    screen.draw.text("Masukkan angka kedua (1-10, 0=10): " + str(factor2), (50, 80), color="black", fontsize=30)
    screen.draw.text("Tekan 1-9 untuk 1-9, 0 untuk 10. ENTER untuk hitung ulang, ESC untuk reset", (50, 500),
                     color="black", fontsize=20)

    if input_mode == 1:
        screen.draw.text("-> Input angka pertama", (450, 50), color="red", fontsize=30)
    elif input_mode == 2:
        screen.draw.text("-> Input angka kedua", (450, 80), color="red", fontsize=30)

    # Tampilkan hasil perkalian
    screen.draw.text(f"{factor1} x {factor2} = {result}", (50, 550), color="blue", fontsize=40)

    # Visualisasi grid (baris x kolom)
    for row in range(factor1):
        for col in range(factor2):
            # Gambar lingkaran sebagai representasi item
            screen.draw.filled_circle((grid_x + col * cell_size, grid_y + row * cell_size), 15, color="green")


def update():
    pass  # Tidak perlu update loop khusus


def on_key_down(key):
    global factor1, factor2, input_mode, result

    if key == keys.ESCAPE:
        # Reset semua ke default
        factor1 = 1
        factor2 = 1
        result = 1
        input_mode = 1

    elif key == keys.RETURN:
        # Hitung hasil
        result = factor1 * factor2

    else:
        value = None
        if keys.K_1 <= key <= keys.K_9:
            value = key - keys.K_0  # 1-9
        elif key == keys.K_0:
            value = 10

        if value is not None and 1 <= value <= 10:
            if input_mode == 1:
                factor1 = value
                input_mode = 2  # Pindah ke input kedua
            elif input_mode == 2:
                factor2 = value
                input_mode = 1  # Kembali ke input pertama
                result = factor1 * factor2  # Hitung otomatis setelah input kedua


pgzrun.go()