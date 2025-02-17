import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Game Constants
GRID_SIZE = 4
TILE_SIZE = 150
MARGIN = 10
WIDTH = GRID_SIZE * (TILE_SIZE + MARGIN) + MARGIN
HEIGHT = WIDTH + 70
FONT = pygame.font.Font(None, 50)
SCORE_FONT = pygame.font.Font(None, 40)
COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (255, 140, 0),
    16: (255, 120, 80),
    32: (255, 100, 60),
    64: (255, 80, 40),
    128: (255, 255, 100),
    256: (255, 255, 80),
    512: (255, 255, 60),
    1024: (255, 255, 40),
    2048: (255, 255, 20)
}

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 Game")

def load_high_score():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0


def save_high_score(score):
    with open("highscore.txt", "w") as file:
        file.write(str(score))

def init_grid():
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    add_new_tile(grid)
    add_new_tile(grid)
    return grid

def add_new_tile(grid):
    empty_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if grid[r][c] == 0]
    if empty_cells:
        r, c = random.choice(empty_cells)
        grid[r][c] = 2 if random.random() < 0.9 else 4

def draw_grid(grid, score):
    screen.fill((50, 50, 50))
    score_text = SCORE_FONT.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            value = grid[r][c]
            color = COLORS.get(value, (255, 255, 255))
            pygame.draw.rect(screen, color, (c * (TILE_SIZE + MARGIN) + MARGIN,
                                             r * (TILE_SIZE + MARGIN) + MARGIN + 50,
                                             TILE_SIZE, TILE_SIZE), border_radius=10)
            if value:
                text = FONT.render(str(value), True, (0, 0, 0))
                text_rect = text.get_rect(center=(c * (TILE_SIZE + MARGIN) + MARGIN + TILE_SIZE // 2,
                                                  r * (TILE_SIZE + MARGIN) + MARGIN + TILE_SIZE // 2 + 50))
                screen.blit(text, text_rect)
    pygame.display.flip()

def merge_left(row):
    new_row = [num for num in row if num != 0]
    score = 0
    for i in range(len(new_row) - 1):
        if new_row[i] == new_row[i + 1]:
            new_row[i] *= 2
            score += new_row[i]
            new_row[i + 1] = 0
    new_row = [num for num in new_row if num != 0]
    return new_row + [0] * (GRID_SIZE - len(new_row)), score

def move(grid, direction):
    rotated = False
    if direction in ('UP', 'DOWN'):
        grid = [list(row) for row in zip(*grid)]
        rotated = True
    if direction in ('RIGHT', 'DOWN'):
        grid = [row[::-1] for row in grid]
    new_grid = []
    total_score = 0
    for row in grid:
        merged_row, score = merge_left(row)
        new_grid.append(merged_row)
        total_score += score
    if direction in ('RIGHT', 'DOWN'):
        new_grid = [row[::-1] for row in new_grid]
    if rotated:
        new_grid = [list(row) for row in zip(*new_grid)]
    return new_grid, total_score

def is_game_over(grid):
    for row in grid:
        if 0 in row:
            return False
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE - 1):
            if grid[r][c] == grid[r][c + 1] or grid[c][r] == grid[c + 1][r]:
                return False
    return True

def game_over_screen():
    screen.fill((30, 30, 30))
    text = FONT.render("Game Over!", True, (255, 0, 0))
    restart_text = SCORE_FONT.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()

def main():
    grid = init_grid()
    score = 0
    running = True
    while running:
        draw_grid(grid, score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    grid, gained_score = move(grid, 'LEFT')
                elif event.key == pygame.K_RIGHT:
                    grid, gained_score = move(grid, 'RIGHT')
                elif event.key == pygame.K_UP:
                    grid, gained_score = move(grid, 'UP')
                elif event.key == pygame.K_DOWN:
                    grid, gained_score = move(grid, 'DOWN')
                else:
                    continue
                score += gained_score
                add_new_tile(grid)
                if is_game_over(grid):
                    game_over_screen()
                    waiting = True
                    while waiting:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_r:
                                    main()
                                elif event.key == pygame.K_q:
                                    pygame.quit()
                                    sys.exit()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()