# Import Libraries
import pygame, sys, random

# Initialize pygame modules
pygame.init()
pygame.font.init()

# Display Variables
WIDTH, HEIGHT = 600, 600
pixel_size = 2
draw_radius = 4

rows, cols = (HEIGHT // pixel_size, WIDTH // pixel_size)
grid = [[0 for i in range(cols)] for j in range(rows)]

clock = pygame.time.Clock()
fps = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
font_render = pygame.font.SysFont('Comic Sans MS', 20)

# Game State class for short term data storage
class GameState:
    def __init__(self):
        self.mouseButton3Held = False
        self.shade_value_direction = -1
        self.min_shade_value = 100
        self.max_shade_value = 255
        self.shade_value = 255
        self.change_shade = 0
        self.change_shade_step = 50
        self.num_particles = 0

game_state = GameState() # Initialize GameState class

# Find point in grid based on variable pixel_size
def find_grid_cell(pos):
    return pos[0] // pixel_size, pos[1] // pixel_size

# Brush function to make spawning new sand particles in a wider area around mouse
def brush_draw(pos):
    if pos[1] - draw_radius >= 0 and pos[1] + draw_radius < rows and pos[0] - draw_radius >= 0 and pos[0] + draw_radius < cols:
        for row in range(pos[1] - draw_radius, pos[1] + draw_radius):
            for col in range(pos[0] - draw_radius, pos[0] + draw_radius):
                grid[row][col] = game_state.shade_value
                game_state.change_shade += 1
                if game_state.change_shade >= game_state.change_shade_step:
                    game_state.change_shade = 0
                    game_state.shade_value += game_state.shade_value_direction
                if game_state.shade_value < game_state.min_shade_value:
                    game_state.shade_value = game_state.min_shade_value
                    game_state.shade_value_direction *= -1
                elif game_state.shade_value > game_state.max_shade_value:
                    game_state.shade_value = game_state.max_shade_value
                    game_state.shade_value_direction *= -1

# Use already implemented functions to count the quantity of particles present in window
def draw_count_text(num_particles):
    text_surface = font_render.render('Particles: {}'.format(num_particles), True, (255, 255, 255))
    screen.blit(text_surface, (WIDTH - 150, 20))

# Necessary function to draw each pixel from the grid to display
def draw_grid_pixels():
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] > 0:
                value = grid[row][col]
                pygame.draw.rect(screen, (value, value, value), pygame.Rect((pixel_size * col, pixel_size * row), (pixel_size, pixel_size)))

# Engine function to apply motion to particles and logic
def move_pixels():
    game_state.num_particles = 0
    for row in range(rows - 1, -1, -1):
        for col in range(cols - 1, -1, -1):
            if grid[row][col] > 0:
                if row + 1 < rows:
                    if grid[row + 1][col] == 0:

                        grid[row + 1][col] = grid[row][col]
                        grid[row][col] = 0
                    elif grid[row + 1][col] > 0:
                        if col - 1 >= 0 and col + 1 < cols:
                            if grid[row + 1][col + 1] == 0 and grid[row + 1][col - 1] > 0:
                                grid[row + 1][col + 1] = grid[row][col]
                                grid[row][col] = 0
                            if grid[row + 1][col - 1] == 0 and grid[row + 1][col + 1] > 0:
                                grid[row + 1][col - 1] = grid[row][col]
                                grid[row][col] = 0
                            if grid[row + 1][col - 1] == 0 and grid[row + 1][col + 1] == 0:
                                direction = random.choice([1, -1])
                                grid[row + 1][col + direction] = grid[row][col]
                                grid[row][col] = 0

                            else:
                                if col + 1 == cols:
                                    if grid[row + 1][col - 1] == 0:
                                        grid[row + 1][col - 1] = grid[row][col]
                                        grid[row][col] = 0

                                if col == 0:
                                    if grid[row + 1][col + 1] == 0:
                                        grid[row + 1][col + 1] = grid[row][col]
                                        grid[row][col] = 0
                game_state.num_particles += 1



running = True

# Main loop
while running:
    for event in pygame.event.get():
        # User exit case
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                game_state.mouseButton3Held = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                game_state.mouseButton3Held = False

    if game_state.mouseButton3Held:
        grid_pos = find_grid_cell(pygame.mouse.get_pos())
        if (0 <= grid_pos[0] <= cols) and (0 <= grid_pos[1] <= rows):
            brush_draw(grid_pos)
    move_pixels()

    screen.fill((0, 0, 0))

    draw_grid_pixels()
    draw_count_text(game_state.num_particles)

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
sys.exit()