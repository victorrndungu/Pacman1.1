import pygame
import sys
import math
import random

# Initialize pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pac-Man with Levels")

# Colors
background_color = (0, 0, 0)   # Black
pacman_color = (255, 255, 0)  # Yellow
ghost_color = (255, 255, 255)  # White
wall_color = (0, 0, 255)      # Blue
dot_color = (0, 255, 255)     # Cyan

# Pac-Man settings
pacman_radius = 20
pacman_x, pacman_y = 100, 100
pacman_speed = 5
mouth_angle = 0
mouth_opening = 15
mouth_direction = 1  # 1 for opening, -1 for closing

# Ghost settings
ghost_radius = 20
ghosts = [
    {"x": 300, "y": 200, "speed_x": 3, "speed_y": 3},
    {"x": 500, "y": 300, "speed_x": -4, "speed_y": 2},
    {"x": 600, "y": 400, "speed_x": 2, "speed_y": -3}
]

# Maze layout for different levels
level_maze_layouts = [
    # Level 1 maze
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ],
    # Level 2 maze (more complex)
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 2, 0, 1, 0, 0, 0, 1, 0, 2, 0, 3, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 2, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 1, 0, 2, 1],
        [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
]

# Cell size
cell_width = width // len(level_maze_layouts[0][0])
cell_height = height // len(level_maze_layouts[0])

# Fonts
font = pygame.font.Font(None, 36)

# Initialize game state
level = 0
score = 0
pacman_x, pacman_y = 100, 100
pacman_speed = 5
ghosts = [
    {"x": 300, "y": 200, "speed_x": 3, "speed_y": 3},
    {"x": 500, "y": 300, "speed_x": -4, "speed_y": 2},
    {"x": 600, "y": 400, "speed_x": 2, "speed_y": -3}
]

# Dots for level
def create_dots(maze_layout):
    return [
        (col * cell_width + cell_width // 2, row * cell_height + cell_height // 2)
        for row, maze_row in enumerate(maze_layout)
        for col, cell in enumerate(maze_row)
        if cell == 0
    ]

dots = create_dots(level_maze_layouts[level])
game_over = False
game_over_time = 0  # For timing the Game Over screen duration

# Draw maze function
def draw_maze(maze_layout):
    for row_index, row in enumerate(maze_layout):
        for col_index, cell in enumerate(row):
            if cell == 1:
                x = col_index * cell_width
                y = row_index * cell_height
                pygame.draw.rect(screen, wall_color, (x, y, cell_width, cell_height))

# Pac-Man drawing with animated mouth
def draw_pacman(x, y, radius, angle):
    start_angle = math.radians(angle)
    end_angle = 2 * math.pi - start_angle
    pygame.draw.circle(screen, pacman_color, (int(x), int(y)), radius)
    pygame.draw.polygon(screen, background_color, [
        (x, y),
        (x + radius * math.cos(start_angle), y - radius * math.sin(start_angle)),
        (x + radius * math.cos(end_angle), y - radius * math.sin(end_angle))
    ])

# Ghost drawing
def draw_ghost(x, y, radius):
    # Ghost body
    pygame.draw.circle(screen, ghost_color, (int(x), int(y - radius // 2)), radius)
    pygame.draw.rect(screen, ghost_color, (x - radius, y - radius // 2, radius * 2, radius))
    # Ghost bottom (wavy effect)
    wave_radius = radius // 4
    for i in range(-2, 3):
        pygame.draw.circle(screen, background_color, (int(x + i * wave_radius), int(y + radius)), wave_radius)
    # Eyes
    eye_radius = radius // 5
    eye_offset_x = radius // 2
    eye_offset_y = radius // 3
    pygame.draw.circle(screen, (0, 0, 0), (int(x - eye_offset_x), int(y - eye_offset_y)), eye_radius)
    pygame.draw.circle(screen, (0, 0, 0), (int(x + eye_offset_x), int(y - eye_offset_y)), eye_radius)

# Check if a position is valid (not colliding with maze walls)
def is_valid_position(x, y, radius, maze_layout):
    pacman_rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
    for row_index, row in enumerate(maze_layout):
        for col_index, cell in enumerate(row):
            if cell == 1:
                wall_rect = pygame.Rect(col_index * cell_width, row_index * cell_height, cell_width, cell_height)
                if pacman_rect.colliderect(wall_rect):
                    return False
    return True

# Move ghosts based on their speed and bounce off the walls
def move_ghosts(maze_layout):
    for ghost in ghosts:
        ghost['x'] += ghost['speed_x']
        ghost['y'] += ghost['speed_y']
        if ghost['x'] <= 0 or ghost['x'] >= width:
            ghost['speed_x'] *= -1
        if ghost['y'] <= 0 or ghost['y'] >= height:
            ghost['speed_y'] *= -1

# Check if Pac-Man collides with any ghosts
def check_collision(pacman_x, pacman_y, pacman_radius):
    for ghost in ghosts:
        distance = math.hypot(pacman_x - ghost['x'], pacman_y - ghost['y'])
        if distance < pacman_radius + ghost_radius:
            return True
    return False

# Display Game Over or You Win screen
def display_game_over(message):
    text = font.render(message, True, (255, 0, 0))
    screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - 30))
    restart_text = font.render("Press Q to Quit", True, (255, 255, 255))
    screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + 30))

# Game loop
clock = pygame.time.Clock()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:  # Press 'Q' to quit the game after Game Over
                game_over = True

    # Movement logic for Pac-Man
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if is_valid_position(pacman_x - pacman_speed, pacman_y, pacman_radius, level_maze_layouts[level]):
            pacman_x -= pacman_speed
    if keys[pygame.K_RIGHT]:
        if is_valid_position(pacman_x + pacman_speed, pacman_y, pacman_radius, level_maze_layouts[level]):
            pacman_x += pacman_speed
    if keys[pygame.K_UP]:
        if is_valid_position(pacman_x, pacman_y - pacman_speed, pacman_radius, level_maze_layouts[level]):
            pacman_y -= pacman_speed
    if keys[pygame.K_DOWN]:
        if is_valid_position(pacman_x, pacman_y + pacman_speed, pacman_radius, level_maze_layouts[level]):
            pacman_y += pacman_speed

    # Animate Pac-Man's mouth opening and closing
    mouth_angle += mouth_opening * mouth_direction
    if mouth_angle >= 30 or mouth_angle <= 0:
        mouth_direction *= -1  # Reverse direction

    # Move ghosts
    move_ghosts(level_maze_layouts[level])

    # Check for collision between Pac-Man and ghosts
    if check_collision(pacman_x, pacman_y, pacman_radius):
        game_over = True

    # Clear the screen
    screen.fill(background_color)

    # Draw maze and dots
    draw_maze(level_maze_layouts[level])
    for dot in dots[:]:
        dot_x, dot_y = dot
        if math.hypot(pacman_x - dot_x, pacman_y - dot_y) < pacman_radius + 5:  # Pac-Man eats the dot
            dots.remove(dot)
            score += 10
        pygame.draw.circle(screen, dot_color, dot, 5)

    # Draw Pac-Man
    draw_pacman(pacman_x, pacman_y, pacman_radius, mouth_angle)

    # Draw ghosts
    for ghost in ghosts:
        draw_ghost(ghost["x"], ghost["y"], ghost_radius)

    # Draw score and level
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    level_text = font.render(f"Level: {level + 1}", True, (255, 255, 255))
    screen.blit(level_text, (width - 120, 10))

    # Check if level is completed
    if not dots:
        level += 1
        if level < len(level_maze_layouts):
            pacman_x, pacman_y = 100, 100  # Reset Pac-Man position
            ghosts = [{"x": random.randint(200, 600), "y": random.randint(100, 400), "speed_x": random.randint(-3, 3), "speed_y": random.randint(-3, 3)} for _ in range(level + 1)]  # Increase ghost count with level
            dots = create_dots(level_maze_layouts[level])
        else:
            game_over = True
            display_game_over("You Win!")

    if game_over:
        display_game_over("Game Over" if not dots else "You Win!")
        game_over_text = font.render("Game Over!", True, (255, 0, 0))
        screen.blit(game_over_text, (width // 2 - 100, height // 2)) # Show game over for a longer time (10 seconds)
        pygame.quit()
        sys.exit()

    pygame.display.flip()
    clock.tick(40)

# Quit the game
pygame.quit()
sys.exit()