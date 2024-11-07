import pygame
import sys
import math
import random

# Initialize pygame modules
pygame.init()

# Screen settings
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pac-Man Game")

# Colors
background_color = (0, 0, 0)
pacman_color = (255, 255, 0)
ghost_color = (255, 0, 0)
wall_color = (0, 0, 255)
dot_color = (0, 255, 255)
confetti_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

# Game settings
pacman = {"x": 80, "y": 100, "radius": 20, "speed": 10, "mouth_angle": 0}
ghosts = [{"x": random.randint(200, width - 100), "y": random.randint(100, height - 100),
           "speed_x": random.choice([-3, 3]), "speed_y": random.choice([-3, 3])} for _ in range(3)]
walls = [pygame.Rect(100, 100, 250, 10), pygame.Rect(450, 100, 250, 10),
         pygame.Rect(100, 490, 600, 10), pygame.Rect(100, 100, 10, 400), pygame.Rect(690, 100, 10, 400)]
dots = [(200 + i * 50, 300) for i in range(10)]
score, game_over, win = 0, False, False
font = pygame.font.Font(None, 36)

# Draw functions
def draw_pacman():
    angle = math.radians(pacman["mouth_angle"])
    pygame.draw.circle(screen, pacman_color, (int(pacman["x"]), int(pacman["y"])), pacman["radius"])
    pygame.draw.polygon(screen, background_color, [
        (pacman["x"], pacman["y"]),
        (pacman["x"] + pacman["radius"] * math.cos(angle), pacman["y"] - pacman["radius"] * math.sin(angle)),
        (pacman["x"] + pacman["radius"] * math.cos(2 * math.pi - angle), pacman["y"] - pacman["radius"] * math.sin(2 * math.pi - angle))
    ])

def draw_confetti():
    for _ in range(100):
        pygame.draw.circle(screen, random.choice(confetti_colors),
                           (random.randint(0, width), random.randint(0, height)), 3)

# Main game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if (game_over or win) and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if restart_button.collidepoint((mouse_x, mouse_y)):
                pacman["x"], pacman["y"], score, game_over, win = 80, 100, 0, False, False
                dots = [(200 + i * 50, 300) for i in range(10)]
            elif exit_button.collidepoint((mouse_x, mouse_y)):
                pygame.quit()
                sys.exit()

    # Game logic if not game over
    if not game_over and not win:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: pacman["x"] -= pacman["speed"]
        if keys[pygame.K_RIGHT]: pacman["x"] += pacman["speed"]
        if keys[pygame.K_UP]: pacman["y"] -= pacman["speed"]
        if keys[pygame.K_DOWN]: pacman["y"] += pacman["speed"]

        # Collision with walls
        pacman_rect = pygame.Rect(pacman["x"] - pacman["radius"], pacman["y"] - pacman["radius"], pacman["radius"] * 2, pacman["radius"] * 2)
        for wall in walls:
            if pacman_rect.colliderect(wall):
                if keys[pygame.K_LEFT]: pacman["x"] += pacman["speed"]
                if keys[pygame.K_RIGHT]: pacman["x"] -= pacman["speed"]
                if keys[pygame.K_UP]: pacman["y"] += pacman["speed"]
                if keys[pygame.K_DOWN]: pacman["y"] -= pacman["speed"]

        pacman["mouth_angle"] = 15 if (pygame.time.get_ticks() // 100) % 2 == 0 else 0

        # Move ghosts and check collision with Pac-Man
        for ghost in ghosts:
            ghost["x"], ghost["y"] = ghost["x"] + ghost["speed_x"], ghost["y"] + ghost["speed_y"]
            if ghost["x"] - pacman["radius"] < 100 or ghost["x"] + pacman["radius"] > 700: ghost["speed_x"] *= -1
            if ghost["y"] - pacman["radius"] < 100 or ghost["y"] + pacman["radius"] > 500: ghost["speed_y"] *= -1
            if math.hypot(pacman["x"] - ghost["x"], pacman["y"] - ghost["y"]) < pacman["radius"] * 2:
                game_over = True

        # Check collision with dots
        eaten_dots = []
        for i, (x, y) in enumerate(dots):
            if math.hypot(pacman["x"] - x, pacman["y"] - y) < pacman["radius"] * 2:
                eaten_dots.append(i)
                score += 10  # Add 10 points for each dot eaten

        # Remove eaten dots
        dots = [dot for i, dot in enumerate(dots) if i not in eaten_dots]

        # Draw and update screen
        screen.fill(background_color)
        for wall in walls: pygame.draw.rect(screen, wall_color, wall)
        for x, y in dots: pygame.draw.circle(screen, dot_color, (x, y), 5)
        draw_pacman()
        for ghost in ghosts: pygame.draw.circle(screen, ghost_color, (int(ghost["x"]), int(ghost["y"])), pacman["radius"])
        screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (10, 10))

        # Win condition
        if not dots: win = True
    else:
        # Display win/lose and buttons
        screen.fill(background_color)
        if win:
            draw_confetti()
            screen.blit(font.render("You Win!", True, (255, 255, 0)), (width // 2 - 50, height // 2 - 40))
        else:
            screen.blit(font.render("Game Over!", True, (255, 0, 0)), (width // 2 - 80, height // 2))
        restart_button, exit_button = pygame.Rect(width // 2 - 100, height // 2 + 40, 100, 50), pygame.Rect(width // 2 + 20, height // 2 + 40, 100, 50)
        pygame.draw.rect(screen, (0, 255, 0), restart_button)
        pygame.draw.rect(screen, (255, 0, 0), exit_button)
        screen.blit(font.render("Restart", True, (0, 0, 0)), (width // 2 - 85, height // 2 + 50))
        screen.blit(font.render("Exit", True, (0, 0, 0)), (width // 2 + 40, height // 2 + 50))

    pygame.display.flip()
    clock.tick(30)
