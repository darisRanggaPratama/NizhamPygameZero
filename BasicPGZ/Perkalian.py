import pgzrun
import pygame

# Initialize variables
WIDTH = 800
HEIGHT = 600
TITLE = "Game Perkalian"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Game states
input_mode = True
show_result = False
first_number = ""
second_number = ""
input_complete = False
current_input = "first"  # or "second"
result = 0
dots = []

def draw():
    screen.fill(WHITE)
    
    if input_mode:
        # Draw input interface
        screen.draw.text("Mari Belajar Perkalian!", center=(WIDTH/2, 50), fontsize=40, color=BLACK)
        screen.draw.text("Masukkan angka pertama: " + first_number, center=(WIDTH/2, 150), fontsize=30, color=BLACK)
        
        if current_input == "second":
            screen.draw.text("Masukkan angka kedua: " + second_number, center=(WIDTH/2, 200), fontsize=30, color=BLACK)
            
        screen.draw.text("Gunakan angka 0-9 untuk input", center=(WIDTH/2, HEIGHT-50), fontsize=20, color=BLUE)
        screen.draw.text("Tekan ENTER untuk lanjut", center=(WIDTH/2, HEIGHT-30), fontsize=20, color=BLUE)
    
    elif show_result:
        # Draw multiplication visualization
        screen.draw.text(f"{first_number} x {second_number} = {result}", center=(WIDTH/2, 50), fontsize=40, color=BLACK)
        
        # Draw dots to visualize multiplication
        for dot in dots:
            screen.draw.filled_circle(dot, 5, BLACK)
        
        screen.draw.text("Tekan SPACE untuk mencoba lagi", center=(WIDTH/2, HEIGHT-30), fontsize=20, color=BLUE)

def on_key_down(key):
    global first_number, second_number, current_input, input_mode, show_result, result, dots, input_complete
    
    if input_mode:
        # Handle number inputs (0-9)
        if key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                  pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
            number = str(key - pygame.K_0)  # Convert key to actual number
            
            if current_input == "first" and len(first_number) < 2:
                first_number += number
            elif current_input == "second" and len(second_number) < 2:
                second_number += number
        
        # Handle enter key
        elif key == pygame.K_RETURN:
            if current_input == "first" and first_number:
                current_input = "second"
            elif current_input == "second" and second_number:
                input_mode = False
                show_result = True
                result = int(first_number) * int(second_number)
                create_visualization()
    
    # Reset game when space is pressed
    elif show_result and key == pygame.K_SPACE:
        reset_game()

def create_visualization():
    global dots
    dots = []
    num1 = int(first_number)
    num2 = int(second_number)
    
    # Calculate dot spacing
    dot_spacing = 20
    start_x = (WIDTH - (min(num1, 10) * dot_spacing)) / 2
    start_y = 150
    
    # Create grid of dots to represent multiplication
    for i in range(num2):
        for j in range(num1):
            x = start_x + (j % 10) * dot_spacing
            y = start_y + (i + (j // 10) * 2) * dot_spacing
            dots.append((x, y))

def reset_game():
    global first_number, second_number, current_input, input_mode
    global show_result, result, dots, input_complete
    
    first_number = ""
    second_number = ""
    current_input = "first"
    input_mode = True
    show_result = False
    result = 0
    dots = []
    input_complete = False

pgzrun.go()
