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
        move_pacman()
        check_wall_collision()
        if move_ghosts():
            game_over = True

        dots = check_dot_collision()
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