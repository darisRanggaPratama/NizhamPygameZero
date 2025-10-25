# Alien Shooter (PyGame Zero)

Game sederhana menembak alien menggunakan PyGame Zero.

Kontrol:
- Panah Kiri / Kanan: Gerak pemain
- Spasi: Menembak
- R: Restart setelah Game Over

Menjalankan:
1. Buat virtual environment (opsional) dan aktifkan.
2. Install dependensi:

```powershell
pip install -r requirements.txt
```

3. Jalankan game dengan pgzrun:

```powershell
pgzrun main.py
```

Atau:

```powershell
python -m pgzero main.py
```

Catatan:
- Script menggunakan shape yang digambar langsung (tidak memerlukan file gambar).
- Jika Anda tidak punya `pgzrun` pada PATH, jalankan `python -m pgzero main.py`.

Enjoy! Selamat mencoba dan kembangkan fitur seperti level, power-up, dan suara.