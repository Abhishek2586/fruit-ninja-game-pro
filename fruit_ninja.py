import pygame
import sys
import os
import random
import json
from pygame import mixer
import math
from enum import Enum

# Game modes
class GameMode(Enum):
    CLASSIC = "classic"
    ARCADE = "arcade"
    ZEN = "zen"
    TUTORIAL = "tutorial"
    CHALLENGE = "challenge"

# Achievement system
class Achievement:
    def __init__(self, name, description, condition, reward):
        self.name = name
        self.description = description
        self.condition = condition
        self.reward = reward
        self.unlocked = False

# Blade system
class BladeType(Enum):
    NORMAL = "normal"
    FIRE = "fire"
    ICE = "ice"
    LIGHTNING = "lightning"

class Blade:
    def __init__(self, blade_type):
        self.type = blade_type
        self.trail_color = {
            BladeType.NORMAL: (255, 255, 255),
            BladeType.FIRE: (255, 69, 0),
            BladeType.ICE: (0, 191, 255),
            BladeType.LIGHTNING: (255, 255, 0)
        }[blade_type]
        self.special_ability = {
            BladeType.NORMAL: lambda: None,
            BladeType.FIRE: lambda: self.burn_nearby_fruits(),
            BladeType.ICE: lambda: self.freeze_fruits(),
            BladeType.LIGHTNING: lambda: self.chain_lightning()
        }[blade_type]

    def burn_nearby_fruits(self):
        # Get all fruits in a radius and apply burn effect
        radius = 100
        for key, value in data.items():
            if value['throw'] and not value['hit']:
                # Calculate distance between blade and fruit
                fruit_center_x = value['x'] + value['img'].get_width() / 2
                fruit_center_y = value['y'] + value['img'].get_height() / 2
                mouse_pos = pygame.mouse.get_pos()
                distance = math.sqrt((fruit_center_x - mouse_pos[0])**2 + (fruit_center_y - mouse_pos[1])**2)
                
                if distance <= radius:
                    # Create fire particles
                    for _ in range(5):
                        particles.append(Particle(fruit_center_x, fruit_center_y, (255, 69, 0)))
                    value['hit'] = True
                    if key != 'bomb':
                        score += 2  # Bonus points for burn effect

    def freeze_fruits(self):
        # Slow down all active fruits
        for value in data.values():
            if value['throw'] and not value['hit']:
                value['speed_x'] *= 0.5
                value['speed_y'] *= 0.5
                # Create ice particles
                fruit_center_x = value['x'] + value['img'].get_width() / 2
                fruit_center_y = value['y'] + value['img'].get_height() / 2
                for _ in range(3):
                    particles.append(Particle(fruit_center_x, fruit_center_y, (0, 191, 255)))

    def chain_lightning(self):
        # Chain lightning between nearby fruits
        hit_fruits = []
        for key1, value1 in data.items():
            if value1['throw'] and not value1['hit']:
                fruit1_center = (value1['x'] + value1['img'].get_width() / 2,
                                value1['y'] + value1['img'].get_height() / 2)
                
                # Find nearby fruits
                for key2, value2 in data.items():
                    if key2 != key1 and value2['throw'] and not value2['hit']:
                        fruit2_center = (value2['x'] + value2['img'].get_width() / 2,
                                        value2['y'] + value2['img'].get_height() / 2)
                        
                        distance = math.sqrt((fruit2_center[0] - fruit1_center[0])**2 +
                                            (fruit2_center[1] - fruit1_center[1])**2)
                        
                        if distance <= 150:  # Chain lightning range
                            hit_fruits.extend([key1, key2])
                            # Create lightning particles between fruits
                            for _ in range(5):
                                particles.append(Particle(
                                    (fruit1_center[0] + fruit2_center[0]) / 2,
                                    (fruit1_center[1] + fruit2_center[1]) / 2,
                                    (255, 255, 0)
                                ))
        
        # Apply damage to chained fruits
        for fruit in set(hit_fruits):  # Remove duplicates
            if fruit != 'bomb':
                data[fruit]['hit'] = True
                score += 3  # Bonus points for chain lightning

# Player variables
player_lives = 3  # Keep track of lives
score = 0  # Keeps track of score
combo_count = 0  # Track consecutive hits
combo_timer = 0  # Timer for combo system
COMBO_TIMEOUT = 1000  # Time window for combos (in milliseconds)
combo_multiplier = 1  # Score multiplier based on combo
bomb_toggle = False  # Track bomb toggle state
all_fruits = ['melon', 'orange', 'pomegranate', 'guava', 'bomb']  # Available fruits for the game
selected_fruits = []  # Fruits selected by the player
player_name = ""  # Player's name
current_game_mode = GameMode.CLASSIC

# Power-up variables
class PowerUpType(Enum):
    SLOW_MOTION = "slow_motion"
    DOUBLE_POINTS = "double_points"
    MEGA_SLICE = "mega_slice"
    FREEZE = "freeze"

power_ups = {
    PowerUpType.SLOW_MOTION: {"active": False, "timer": 0, "duration": 5000, "factor": 0.5},
    PowerUpType.DOUBLE_POINTS: {"active": False, "timer": 0, "duration": 7000},
    PowerUpType.MEGA_SLICE: {"active": False, "timer": 0, "duration": 3000},
    PowerUpType.FREEZE: {"active": False, "timer": 0, "duration": 4000}
}

# Particle system
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 5)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 5)
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed
        self.lifetime = 255

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.dy += 0.1  # Gravity
        self.lifetime -= 5
        return self.lifetime > 0

    def draw(self, surface):
        alpha = max(0, min(255, self.lifetime))
        color = (*self.color, alpha)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.size)

particles = []  # List to store active particles

# Initialize sound mixer
pygame.mixer.init()
slice_sound = pygame.mixer.Sound(os.path.join('fruit-ninja-game-python-code', 'sounds', 'slice.wav'))
explosion_sound = pygame.mixer.Sound(os.path.join('fruit-ninja-game-python-code', 'sounds', 'explosion.wav'))

# Load high scores
def load_high_scores():
    try:
        with open('highscores.json', 'r') as f:
            return json.load(f)['high_scores']
    except:
        return []

def save_high_score(player_name, score):
    high_scores = load_high_scores()
    high_scores.append({'name': player_name, 'score': score})
    high_scores.sort(key=lambda x: x['score'], reverse=True)
    high_scores = high_scores[:5]  # Keep only top 5 scores
    with open('highscores.json', 'w') as f:
        json.dump({'high_scores': high_scores}, f, indent=4)

# Achievement definitions
achievements = [
    Achievement("Fruit Ninja Master", "Score 100 points in a single game", lambda s: s >= 100, "Unlock Fire Blade"),
    Achievement("Combo King", "Get a 10x combo", lambda c: c >= 10, "Unlock Ice Blade"),
    Achievement("Survivor", "Play 5 games", lambda g: g >= 5, "Unlock Lightning Blade"),
    Achievement("Perfect Slice", "Hit 5 fruits in a row", lambda c: c >= 5, "Double Points Duration +2s")
]

# Background themes based on score
background_themes = {
    0: pygame.image.load(os.path.join('fruit-ninja-game-python-code', 'back.jpg')),
    50: pygame.image.load(os.path.join('fruit-ninja-game-python-code', 'back1.jpg')),
}

# Current blade type
current_blade = Blade(BladeType.NORMAL)
games_played = 0

# Function to update achievements
def check_achievements():
    global power_ups, current_blade
    for achievement in achievements:
        if not achievement.unlocked:
            if achievement.name == "Fruit Ninja Master" and achievement.condition(score):
                achievement.unlocked = True
                current_blade = Blade(BladeType.FIRE)
            elif achievement.name == "Combo King" and achievement.condition(combo_count):
                achievement.unlocked = True
                current_blade = Blade(BladeType.ICE)
            elif achievement.name == "Survivor" and achievement.condition(games_played):
                achievement.unlocked = True
                current_blade = Blade(BladeType.LIGHTNING)
            elif achievement.name == "Perfect Slice" and achievement.condition(combo_count):
                achievement.unlocked = True
                power_ups[PowerUpType.DOUBLE_POINTS]["duration"] += 2000

# Function to get current background based on score
def get_current_background(score):
    current_theme = 0
    for threshold in sorted(background_themes.keys()):
        if score >= threshold:
            current_theme = threshold
    return background_themes[current_theme]

# Initialize pygame and create window
WIDTH = 800
HEIGHT = 500
FPS = 12  # Controls the refresh rate
pygame.init()
pygame.display.set_caption('Fruit-Ninja Game -- DataFlair')
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))  # Game display size
clock = pygame.time.Clock()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Load assets
background = pygame.image.load(os.path.join('fruit-ninja-game-python-code', 'back.jpg'))  # Game background
font = pygame.font.Font(os.path.join('fruit-ninja-game-python-code', 'comic.ttf'), 42)
lives_icon = pygame.image.load(os.path.join('fruit-ninja-game-python-code', 'images', 'white_lives.png'))  # Lives icon

# Function to generate random fruits
def generate_random_fruits(fruit):
    
    fruit_path = os.path.join('fruit-ninja-game-python-code', 'images', fruit + '.png')
    data[fruit] = {
        'img': pygame.image.load(fruit_path),
        'x': random.randint(100, 500),  # Position on x-coordinate
        'y': 800,
        'speed_x': random.randint(-10, 10),  # Speed in x direction
        'speed_y': random.randint(-80, -60),  # Speed in y direction
        'throw': False,  # Whether the fruit is outside the game window
        't': 0,
        'hit': False,
    }

    if random.random() >= 0.75:
        data[fruit]['throw'] = True
    else:
        data[fruit]['throw'] = False

# Dictionary to hold the random fruit data
data = {}
for fruit in all_fruits:
    generate_random_fruits(fruit)

# Function to hide crossed-out lives
def hide_cross_lives(x, y):
    try:
        gameDisplay.blit(pygame.image.load(os.path.join('fruit-ninja-game-python-code', 'images', 'red_lives.png')), (x, y))
    except:
        pass

# Function to draw text on the screen
def draw_text(display, text, size, x, y, color=WHITE):
    font = pygame.font.Font(pygame.font.match_font('comic.ttf'), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    display.blit(text_surface, text_rect)

# Function to draw player's lives
def draw_bomb_toggle(display, x, y, state):
    # Draw checkbox
    checkbox_rect = pygame.Rect(x, y, 20, 20)
    pygame.draw.rect(display, WHITE, checkbox_rect, 2)
    if state:
        # Draw checkmark
        pygame.draw.line(display, WHITE, (x+3, y+10), (x+8, y+15), 2)
        pygame.draw.line(display, WHITE, (x+8, y+15), (x+17, y+5), 2)
    # Draw label
    font = pygame.font.Font(None, 24)
    text = font.render("Bombs", True, WHITE)
    display.blit(text, (x + 30, y))

def draw_lives(display, x, y, lives, image):
    for i in range(lives):
        try:
            img = pygame.image.load(os.path.join('fruit-ninja-game-python-code', 'images', image))
            img_rect = img.get_rect()
            img_rect.x = int(x + 35 * i)
            img_rect.y = y
            display.blit(img, img_rect)
        except:
            pass

# Function to show the registration screen with player info
def registration_screen():
    global player_name
    input_active = True
    input_box = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    player_name = ""
    title_particles = []
    title_animation_time = 0
    logo = pygame.image.load(os.path.join('fruit-ninja-game-python-code', 'images', 'logo.png'))
    logo = pygame.transform.scale(logo, (300, 150))
    pulse_effect = 0

    while input_active:
        current_time = pygame.time.get_ticks()
        pulse_effect += 0.05

        # Create dynamic background with multiple color layers
        for y in range(HEIGHT):
            color_value = int(255 * (1 - y / HEIGHT))
            wave = math.sin(y / 50 + pulse_effect) * 20
            pygame.draw.line(gameDisplay, 
                (int(color_value * 0.2), int(color_value * 0.4), color_value),
                (0 + wave, y), (WIDTH + wave, y))

        # Animated title effect with pulse
        title_animation_time += 0.05
        title_scale = 1.0 + 0.15 * math.sin(title_animation_time)
        glow_intensity = abs(math.sin(title_animation_time))
        
        # Add glow effect to logo
        glow_surface = pygame.Surface((300 * title_scale + 20, 150 * title_scale + 20), pygame.SRCALPHA)
        pygame.draw.ellipse(glow_surface, 
            (255, 255, 255, int(100 * glow_intensity)),
            glow_surface.get_rect())
        glow_rect = glow_surface.get_rect(center=(WIDTH // 2, HEIGHT // 6))
        gameDisplay.blit(glow_surface, glow_rect)

        scaled_logo = pygame.transform.scale(logo, 
            (int(300 * title_scale), int(150 * title_scale)))
        logo_rect = scaled_logo.get_rect(center=(WIDTH // 2, HEIGHT // 6))
        gameDisplay.blit(scaled_logo, logo_rect)

        # Enhanced input box with dynamic border
        border_thickness = 2 + math.sin(pulse_effect) * 1
        border_color = (
            int(color[0] * (1 + math.sin(current_time/500))/2),
            int(color[1] * (1 + math.sin(current_time/700))/2),
            int(color[2] * (1 + math.sin(current_time/900))/2)
        )
        
        # Draw multiple borders for glow effect
        for i in range(3):
            pygame.draw.rect(gameDisplay, border_color,
                input_box.inflate(8 - i*2, 8 - i*2), int(border_thickness))

        # Player's info box with animated gradient
        info_box = pygame.Rect(WIDTH // 4, HEIGHT // 2 + 60, WIDTH // 2, 120)
        gradient_color = (0, int(100 + 50 * math.sin(pulse_effect)), int(200 + 55 * math.sin(pulse_effect)))
        pygame.draw.rect(gameDisplay, (*gradient_color, 100), info_box)
        pygame.draw.rect(gameDisplay, (*gradient_color, 255), info_box, 2)

        # Enhanced text rendering with glow
        title_color = (255, 
            int(200 + 55 * math.sin(pulse_effect)),
            int(100 + 55 * math.cos(pulse_effect)))
        draw_text(gameDisplay, "Enter Your Name:", 40, WIDTH // 2, HEIGHT // 3, title_color)

        # Player's info with dynamic icons
        draw_text(gameDisplay, "Starting Info:", 30, WIDTH // 2, HEIGHT // 2 + 80)
        lives_img = pygame.image.load(os.path.join('fruit-ninja-game-python-code', 'images', 'white_lives.png'))
        lives_img = pygame.transform.scale(lives_img, (20, 20))
        lives_pos = (WIDTH // 2 - 100 + math.sin(pulse_effect) * 5, HEIGHT // 2 + 120)
        gameDisplay.blit(lives_img, lives_pos)
        
        # Animated score display
        score_color = (max(0, min(255, int(100 + 155 * math.sin(pulse_effect)))),
                      255,
                      max(0, min(255, int(100 + 155 * math.cos(pulse_effect)))))
        draw_text(gameDisplay, f": {player_lives}", 25, WIDTH // 2 - 60, HEIGHT // 2 + 120, score_color)
        draw_text(gameDisplay, f"Starting Score: {score}", 25, WIDTH // 2, HEIGHT // 2 + 150, score_color)

        # Input text with enhanced shadow
        font = pygame.font.Font(None, 42)
        shadow_offset = 2 + math.sin(pulse_effect)
        shadow_surface = font.render(player_name, True, (30, 30, 30))
        text_surface = font.render(player_name, True, WHITE)
        gameDisplay.blit(shadow_surface, (input_box.x + shadow_offset + 10, input_box.y + shadow_offset + 10))
        gameDisplay.blit(text_surface, (input_box.x + 10, input_box.y + 10))

        # Dynamic instruction text
        instruction_color = (255, 255, int(255 * (1 + math.sin(current_time/300))/2))
        instruction_scale = 1.0 + 0.1 * math.sin(pulse_effect * 2)
        draw_text(gameDisplay, "Press ENTER to Continue", int(30 * instruction_scale), 
                 WIDTH // 2, HEIGHT - 50, instruction_color)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                    for _ in range(15):  # Increased particle count
                        title_particles.append(Particle(
                            event.pos[0], event.pos[1],
                            (random.randint(100, 255), random.randint(100, 255), 255)))
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if player_name:  # Ensure player name is not empty
                            input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                        # Add delete effect particles
                        for _ in range(5):
                            title_particles.append(Particle(
                                input_box.right, input_box.centery,
                                (255, 100, 100)))
                    else:
                        player_name += event.unicode
                        # Add typing effect particles
                        for _ in range(3):
                            title_particles.append(Particle(
                                input_box.right, input_box.centery,
                                (100, 255, 100)))

        # Update and draw particles with improved effects
        title_particles = [p for p in title_particles if p.update()]
        for particle in title_particles:
            particle.draw(gameDisplay)

        pygame.display.flip()
        clock.tick(FPS)

# Function to show fruit selection screen
def choose_fruits_screen():
    global selected_fruits
    selecting = True
    selected_fruits = []  # Clear previous selections
    animation_time = 0
    fruit_hover = None
    fruit_images = {}
    fruit_rects = {}
    hover_scale = 1.0
    hover_direction = 1

    # Load and scale fruit images with effects
    for fruit in all_fruits:
        img = pygame.image.load(os.path.join('fruit-ninja-game-python-code', 'images', f'{fruit}.png'))
        fruit_images[fruit] = pygame.transform.scale(img, (80, 80))

    while selecting:
        current_time = pygame.time.get_ticks()
        animation_time += 0.05
        hover_scale += 0.01 * hover_direction
        if hover_scale >= 1.2 or hover_scale <= 1.0:
            hover_direction *= -1

        # Create animated gradient background with waves
        for y in range(HEIGHT):
            wave = math.sin(y / 30 + animation_time) * 10
            color_value = int(128 + 64 * math.sin(y / 50 + animation_time))
            pygame.draw.line(gameDisplay,
                (int(color_value * 0.3), int(color_value * 0.5), color_value),
                (0 + wave, y), (WIDTH + wave, y))

        # Enhanced title with glow effect
        title_color = (255, 
            int(200 + 55 * math.sin(animation_time * 2)),
            int(200 + 55 * math.cos(animation_time * 2)))
        glow_surface = pygame.Surface((400, 100), pygame.SRCALPHA)
        pygame.draw.ellipse(glow_surface,
            (*title_color[:3], 50),
            glow_surface.get_rect())
        gameDisplay.blit(glow_surface,
            glow_surface.get_rect(center=(WIDTH // 2, HEIGHT // 6)))
        draw_text(gameDisplay, "Choose Your Fruits", 60, WIDTH // 2, HEIGHT // 6, title_color)

        # Create an enhanced grid layout for fruits
        grid_start_x = WIDTH // 4
        grid_start_y = HEIGHT // 3
        grid_spacing_x = WIDTH // 4
        grid_spacing_y = HEIGHT // 4

        # Display fruits with hover and selection effects
        mouse_pos = pygame.mouse.get_pos()
        fruit_rects.clear()

        for index, fruit in enumerate(all_fruits):
            row = index // 2
            col = index % 2
            base_x = grid_start_x + col * grid_spacing_x
            base_y = grid_start_y + row * grid_spacing_y

            # Calculate fruit position with floating animation
            float_offset = math.sin(animation_time * 2 + index) * 10
            x = base_x - 30
            y = base_y + float_offset

            # Create fruit rect for collision detection
            fruit_rect = pygame.Rect(x, y, 80, 80)
            fruit_rects[fruit] = fruit_rect

            # Apply hover and selection effects
            scale = hover_scale if fruit == fruit_hover else 1.0
            if fruit in selected_fruits:
                scale *= 1.1

            # Draw selection highlight
            if fruit in selected_fruits:
                glow = pygame.Surface((100, 100), pygame.SRCALPHA)
                glow_color = (255, 215, 0, int(100 + 50 * math.sin(animation_time * 3)))
                pygame.draw.circle(glow, glow_color, (50, 50), 45)
                gameDisplay.blit(glow, (x - 10, y - 10))

            # Draw fruit with effects
            scaled_img = pygame.transform.scale(fruit_images[fruit],
                (int(80 * scale), int(80 * scale)))
            img_rect = scaled_img.get_rect(center=(x + 40, y + 40))
            gameDisplay.blit(scaled_img, img_rect)

            # Draw fruit name with shadow
            name_color = (255, 255, 255) if fruit in selected_fruits else (200, 200, 200)
            shadow_color = (0, 0, 0)
            draw_text(gameDisplay, fruit.capitalize(), 20, x + 40, y + 90, shadow_color)
            draw_text(gameDisplay, fruit.capitalize(), 20, x + 38, y + 88, name_color)

        # Update hover state
        fruit_hover = None
        for fruit, rect in fruit_rects.items():
            if rect.collidepoint(mouse_pos):
                fruit_hover = fruit
                break

        # Draw continue button with effects
        continue_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 80, 200, 50)
        btn_color = (0, 200, 100) if len(selected_fruits) >= 3 else (100, 100, 100)
        btn_glow = pygame.Surface((220, 70), pygame.SRCALPHA)
        glow_alpha = int(100 + 50 * math.sin(animation_time * 3))
        pygame.draw.rect(btn_glow, (*btn_color, glow_alpha), btn_glow.get_rect(), border_radius=10)
        gameDisplay.blit(btn_glow, (WIDTH // 2 - 110, HEIGHT - 90))
        pygame.draw.rect(gameDisplay, btn_color, continue_btn, border_radius=10)
        draw_text(gameDisplay, "Continue", 30, WIDTH // 2, HEIGHT - 65,
                 (255, 255, 255) if len(selected_fruits) >= 3 else (150, 150, 150))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle fruit selection
                for fruit, rect in fruit_rects.items():
                    if rect.collidepoint(event.pos):
                        if fruit in selected_fruits:
                            selected_fruits.remove(fruit)
                        elif len(selected_fruits) < 4 and fruit != 'bomb':
                            selected_fruits.append(fruit)
                            # Add selection particles
                            for _ in range(10):
                                particles.append(Particle(
                                    rect.centerx, rect.centery,
                                    (255, 215, 0)))

                # Handle continue button
                if continue_btn.collidepoint(event.pos) and len(selected_fruits) >= 3:
                    selecting = False

        # Update and draw particles
        particles[:] = [p for p in particles if p.update()]
        for particle in particles:
            particle.draw(gameDisplay)

        # Draw selection counter
        counter_text = f"Selected: {len(selected_fruits)}/4"
        draw_text(gameDisplay, counter_text, 30, WIDTH // 2, HEIGHT - 120,
                 (255, 255, 255) if len(selected_fruits) >= 3 else (200, 100, 100))

        pygame.display.flip()
        clock.tick(FPS)

    return selected_fruits

# Helper function to toggle fruit selection
def toggle_fruit_selection(fruit):
    if fruit in selected_fruits:
        selected_fruits.remove(fruit)  # Deselect the fruit
    else:
        selected_fruits.append(fruit)  # Select the fruit

# Function to show game over screen
def show_gameover_screen():
    global score, player_name
    save_high_score(player_name, score)  # Save the score before showing game over screen
    current_background = get_current_background(score)
    gameDisplay.blit(current_background, (0, 0))
    
    # Draw achievements
    achievement_y = 150
    for achievement in achievements:
        if achievement.unlocked:
            draw_text(gameDisplay, f"✓ {achievement.name}", 15, WIDTH - 100, achievement_y, GREEN)
        achievement_y += 20
    draw_text(gameDisplay, "FRUIT NINJA!", 90, WIDTH / 2, HEIGHT / 4)
    draw_text(gameDisplay, "Score : " + str(score), 50, WIDTH / 2, HEIGHT / 2)
    draw_text(gameDisplay, "Press R to Replay", 50, WIDTH / 2, HEIGHT * 3 / 4 - 50)
    draw_text(gameDisplay, "Press Q to Quit", 50, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    return True  # Return True to indicate replay
                elif event.key == pygame.K_q:
                    return False  # Return False to indicate quit

# Game Loop
first_round = True
game_over = True
game_running = True
while game_running:
    if game_over:
        if first_round:
            registration_screen()  # Call the registration screen first
            first_round = False
            choose_fruits_screen()  # Call fruit selection screen after registration
        game_over = False
        player_lives = 3
        score = 0
        games_played += 1
        check_achievements()
        # Clear and regenerate fruit data for new game
        data.clear()
        for fruit in selected_fruits + (['bomb'] if bomb_toggle else []):  # Generate fruits including bombs if toggled
            generate_random_fruits(fruit)
        draw_lives(gameDisplay, 690, 5, player_lives, 'red_lives.png')

    current_time = pygame.time.get_ticks()

    # Update combo system
    if current_time - combo_timer > COMBO_TIMEOUT:
        combo_count = 0
        combo_multiplier = 1

    # Update power-ups
    for power_up_type, power_up in power_ups.items():
        if power_up['active'] and current_time - power_up['timer'] > power_up['duration']:
            power_up['active'] = False

    # Update particles
    particles[:] = [p for p in particles if p.update()]
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if bomb toggle was clicked
            mouse_pos = pygame.mouse.get_pos()
            if 700 < mouse_pos[0] < 720 and 50 < mouse_pos[1] < 70:
                bomb_toggle = not bomb_toggle
                # Update bomb in data based on toggle state
                if bomb_toggle and 'bomb' not in data:
                    generate_random_fruits('bomb')
                elif not bomb_toggle and 'bomb' in data:
                    del data['bomb']

    current_background = get_current_background(score)
    gameDisplay.blit(current_background, (0, 0))
    
    # Draw achievements
    achievement_y = 150
    for achievement in achievements:
        if achievement.unlocked:
            draw_text(gameDisplay, f"✓ {achievement.name}", 15, WIDTH - 100, achievement_y, GREEN)
        achievement_y += 20
    draw_text(gameDisplay, "Score : " + str(score), 42, WIDTH // 2, 10)
    if combo_count > 1:
        draw_text(gameDisplay, f"Combo x{combo_count}", 30, WIDTH // 2, 50, YELLOW)
    draw_lives(gameDisplay, 690, 5, player_lives, 'red_lives.png')
    draw_bomb_toggle(gameDisplay, 700, 50, bomb_toggle)

    # Draw active power-ups
    power_up_y = 100
    for power_up_type, power_up in power_ups.items():
        if power_up['active']:
            draw_text(gameDisplay, f"{power_up_type.value}: {(power_up['duration'] - (current_time - power_up['timer'])) // 1000}s", 20, WIDTH - 100, power_up_y, GREEN)
            power_up_y += 30

    # Draw particles
    for particle in particles:
        particle.draw(gameDisplay)

    for key, value in data.items():
        if value['throw'] and (key != 'bomb' or (key == 'bomb' and bomb_toggle)):
            # Apply slow motion if active
            speed_multiplier = power_ups[PowerUpType.SLOW_MOTION]['factor'] if power_ups[PowerUpType.SLOW_MOTION]['active'] else 1.0
            
            value['x'] += value['speed_x'] * speed_multiplier
            value['y'] += value['speed_y'] * speed_multiplier
            value['speed_y'] += (1 * value['t']) * speed_multiplier
            value['t'] += 1 * speed_multiplier

            if value['y'] <= 800:
                gameDisplay.blit(value['img'], (value['x'], value['y']))  # Displaying fruit
            else:
                # Only regenerate if it's not a bomb or if bomb toggle is on
                if key != 'bomb' or bomb_toggle:
                    generate_random_fruits(key)

            current_position = pygame.mouse.get_pos()  # Get the current mouse position

            fruit_width = value['img'].get_width()
            fruit_height = value['img'].get_height()

            if not value['hit'] and value['x'] < current_position[0] < value['x'] + fruit_width \
                    and value['y'] < current_position[1] < value['y'] + fruit_height:
                if key == 'bomb':
                    explosion_sound.play()
                    player_lives -= 1
                    combo_count = 0  # Reset combo on bomb hit
                    
                    # Create explosion particles
                    for _ in range(20):
                        particles.append(Particle(value['x'] + fruit_width/2, value['y'] + fruit_height/2, (255, 165, 0)))
                    
                    if player_lives == 0:
                        hide_cross_lives(690, 15)
                    elif player_lives == 1:
                        hide_cross_lives(725, 15)
                    elif player_lives == 2:
                        hide_cross_lives(760, 15)

                    if player_lives < 0:
                        replay = show_gameover_screen()
                        if replay:
                            first_round = True
                            game_over = True
                        else:
                            game_running = False

                    try:
                        half_fruit_path = os.path.join('fruit-ninja-game-python-code', 'images', "explosion.png")
                    except:
                        half_fruit_path = None
                else:
                    try:
                        half_fruit_path = os.path.join('fruit-ninja-game-python-code', 'images', "half_" + key + ".png")
                    except:
                        half_fruit_path = None

                    # Update combo system
                    combo_count += 1
                    combo_timer = current_time
                    combo_multiplier = min(4, 1 + combo_count // 3)  # Cap multiplier at 4x

                    # Create juice particles
                    fruit_color = {
                        'apple': (255, 0, 0),
                        'orange': (255, 165, 0),
                        'pomegranate': (255, 0, 0),
                        'guava': (173, 255, 47),
                        'melon': (50, 205, 50)
                    }.get(key, (255, 0, 0))
                    
                    for _ in range(10):
                        particles.append(Particle(value['x'] + fruit_width/2, value['y'] + fruit_height/2, fruit_color))

                value['img'] = pygame.image.load(half_fruit_path)
                value['speed_x'] += 10
                if key != 'bomb':
                    slice_sound.play()
                    # Calculate points with combo multiplier and power-ups
                    points = 1 * combo_multiplier
                    if power_ups[PowerUpType.DOUBLE_POINTS]['active']:
                        points *= 2
                    score += int(points)
                    
                    # Random chance to activate power-ups
                    if random.random() < 0.1:  # 10% chance
                        power_up_type = random.choice(list(PowerUpType))
                        if not power_ups[power_up_type]['active']:
                            power_ups[power_up_type]['active'] = True
                            power_ups[power_up_type]['timer'] = current_time
                            
                value['hit'] = True
        else:
            # Only regenerate if it's not a bomb or if bomb toggle is on
            if key != 'bomb' or bomb_toggle:
                generate_random_fruits(key)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
